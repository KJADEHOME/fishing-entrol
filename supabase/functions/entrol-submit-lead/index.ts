import { createClient } from "npm:@supabase/supabase-js@2";
import { assessLeadAbuse } from "./anti-spam.mjs";

type BusinessUnit = "pet_products" | "socks" | "kjadehome";

type SiteConfig = {
  businessUnit: BusinessUnit;
  sourceSite: "www.entrol.com" | "entrol.com" | "socks.entrol.com" | "www.kjadehome.com" | "kjadehome.com";
  notificationLabel: "Entrol Pet Lead" | "Entrol Socks Lead" | "KJadeHome Lead";
  notificationIntro: string;
  notificationToEnv: "ENTROL_NOTIFICATION_TO" | "ENTROL_SOCKS_NOTIFICATION_TO";
  notificationFromEnv: "ENTROL_NOTIFICATION_FROM" | "ENTROL_SOCKS_NOTIFICATION_FROM";
  customerReplyFromEnv: "ENTROL_CUSTOMER_REPLY_FROM" | "ENTROL_SOCKS_CUSTOMER_REPLY_FROM";
};

// The browser cannot choose its business unit. The request Origin is matched
// against this server-owned map before any payload field is read or stored.
const SITE_BY_ORIGIN: Readonly<Record<string, SiteConfig>> = Object.freeze({
  "https://www.entrol.com": {
    businessUnit: "pet_products",
    sourceSite: "www.entrol.com",
    notificationLabel: "Entrol Pet Lead",
    notificationIntro: "A new Entrol pet-products website lead was stored successfully.",
    notificationToEnv: "ENTROL_NOTIFICATION_TO",
    notificationFromEnv: "ENTROL_NOTIFICATION_FROM",
    customerReplyFromEnv: "ENTROL_CUSTOMER_REPLY_FROM",
  },
  "https://entrol.com": {
    businessUnit: "pet_products",
    sourceSite: "entrol.com",
    notificationLabel: "Entrol Pet Lead",
    notificationIntro: "A new Entrol pet-products website lead was stored successfully.",
    notificationToEnv: "ENTROL_NOTIFICATION_TO",
    notificationFromEnv: "ENTROL_NOTIFICATION_FROM",
    customerReplyFromEnv: "ENTROL_CUSTOMER_REPLY_FROM",
  },
  "https://socks.entrol.com": {
    businessUnit: "socks",
    sourceSite: "socks.entrol.com",
    notificationLabel: "Entrol Socks Lead",
    notificationIntro: "A new Entrol socks website lead was stored successfully.",
    notificationToEnv: "ENTROL_SOCKS_NOTIFICATION_TO",
    notificationFromEnv: "ENTROL_SOCKS_NOTIFICATION_FROM",
    customerReplyFromEnv: "ENTROL_SOCKS_CUSTOMER_REPLY_FROM",
  },
  "https://www.kjadehome.com": {
    businessUnit: "kjadehome",
    sourceSite: "www.kjadehome.com",
    notificationLabel: "KJadeHome Lead",
    notificationIntro: "A new KJadeHome website lead was stored successfully.",
    notificationToEnv: "ENTROL_NOTIFICATION_TO",
    notificationFromEnv: "ENTROL_NOTIFICATION_FROM",
    customerReplyFromEnv: "ENTROL_CUSTOMER_REPLY_FROM",
  },
  "https://kjadehome.com": {
    businessUnit: "kjadehome",
    sourceSite: "kjadehome.com",
    notificationLabel: "KJadeHome Lead",
    notificationIntro: "A new KJadeHome website lead was stored successfully.",
    notificationToEnv: "ENTROL_NOTIFICATION_TO",
    notificationFromEnv: "ENTROL_NOTIFICATION_FROM",
    customerReplyFromEnv: "ENTROL_CUSTOMER_REPLY_FROM",
  },
});

// Disposable / tenant email domains that spammers abuse to fake a "business" address.
const SUSPICIOUS_EMAIL_DOMAINS = new Set([
  "onmicrosoft.com",
  "razorvision.net",
  "mailinator.com", "tempmail.com", "guerrillamail.com", "10minutemail.com",
  "yopmail.com", "trashmail.com", "getnada.com", "sharklasers.com", "throwawaymail.com",
  "dispostable.com", "fakeinbox.com", "maildrop.cc", "temp-mail.org", "mailnesia.com",
]);

// Recognised destination markets / countries. Used to reject gibberish "target market" spam.
const MARKET_KEYWORD_RE = /\b(us|usa|u\.s\.a?|uk|u\.k|eu|europe|european|eea|emea|united states|united kingdom|states|england|scotland|wales|britain|great britain|germany|german|france|french|spain|spanish|italy|italian|netherlands|holland|belgium|switzerland|austria|sweden|norway|denmark|finland|poland|portugal|ireland|greece|romania|czech|hungary|australia|australian|new zealand|nz|asia|japan|japanese|korea|korean|china|chinese|singapore|malaysia|thailand|vietnam|india|indonesia|philippines|canada|mexico|brazil|latin america|latam|south america|north america|middle east|uae|saudi|africa|south africa|oceania|global|worldwide|world|international|overseas)\b/i;

function isPlausibleMarket(text: string | null): boolean {
  if (!text) return false;
  const normalized = text.trim();
  if (normalized.length === 0) return false;
  if (MARKET_KEYWORD_RE.test(normalized)) return true;
  if (/\s/.test(normalized) && normalized.length <= 60) return true;
  return false;
}

// Detect random-letter gibberish used in spammer "name" / "company" fields
// (e.g. "Nukbs LLC", "kGxbsrYoSMaGfKgk"). Conservative: a multi-word phrase is
// only flagged on a very long consonant run so real names like "John Smith" survive.
function isGibberishName(text: string | null): boolean {
  if (!text) return false;
  const t = text.trim();
  if (t.length < 3 || t.length > 60) return false;
  const hasSpace = /\s/.test(t);
  const tokens = t.split(/\s+/).filter(Boolean);
  for (const tok of tokens) {
    const letters = tok.replace(/[^a-zA-Z]/g, "");
    if (letters.length < 3) continue;
    const vowels = (letters.match(/[aeiouAEIOU]/g) || []).length;
    const ratio = vowels / letters.length;
    const runs = letters.match(/[^aeiouAEIOU]+/g) || [];
    const consMax = runs.reduce((m, s) => Math.max(m, s.length), 0);
    if (hasSpace) {
      if (consMax >= 5) return true;
    } else if (consMax >= 4 && ratio <= 0.25 && letters.length >= 5) {
      return true;
    }
  }
  return false;
}

const MAX_BODY_BYTES = 24_000;
const TEXT_LIMITS: Record<string, number> = {
  name: 160,
  email: 320,
  contact: 320,
  company: 240,
  product_interest: 500,
  quantity: 160,
  target_market: 240,
  message: 5000,
  source_page: 2000,
  landing_page: 2000,
  referrer: 2000,
  utm_source: 240,
  utm_medium: 240,
  utm_campaign: 240,
  utm_content: 500,
  utm_term: 500,
  catalog_touch_page: 2000,
  catalog_touch_placement: 80,
  catalog_touched_at: 80,
  inquiry_trigger: 500,
};

function siteForOrigin(origin: string | null): SiteConfig | null {
  return origin ? SITE_BY_ORIGIN[origin] || null : null;
}

function corsHeaders(origin: string | null): Record<string, string> {
  const headers: Record<string, string> = {
    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-request-id, x-retry-count, traceparent, tracestate, baggage",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
  if (siteForOrigin(origin)) headers["Access-Control-Allow-Origin"] = origin as string;
  return headers;
}

function jsonResponse(origin: string | null, body: unknown, status: number) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders(origin), "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
  });
}

function clean(value: unknown, max: number): string | null {
  if (typeof value !== "string") return null;
  const normalized = value.trim().replace(/\u0000/g, "");
  return normalized ? normalized.slice(0, max) : null;
}

function first(payload: Record<string, unknown>, names: string[], max: number): string | null {
  for (const name of names) {
    const value = clean(payload[name], max);
    if (value) return value;
  }
  return null;
}

function cleanTimestamp(value: unknown): string | null {
  const text = clean(value, TEXT_LIMITS.catalog_touched_at);
  if (!text) return null;
  const parsed = Date.parse(text);
  return Number.isFinite(parsed) ? new Date(parsed).toISOString() : null;
}

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

type ScorableLead = {
  name: string | null;
  email: string | null;
  contact: string | null;
  company: string | null;
  product_interest: string | null;
  quantity: string | null;
  target_market: string | null;
  message: string | null;
  utm_source: string | null;
  catalog_touch_page: string | null;
  catalog_touch_placement: string | null;
};

function scoreLead(lead: ScorableLead) {
  let score = 0;
  const reasons: string[] = [];
  const spamSignals: string[] = [];
  const add = (points: number, reason: string) => {
    score += points;
    reasons.push(`${reason} (+${points})`);
  };

  if (lead.company) {
    if (isGibberishName(lead.company)) {
      score -= 5;
      reasons.push("company name looks like gibberish (-5)");
      spamSignals.push("company name is gibberish");
    } else {
      add(15, "company provided");
    }
  }
  if (lead.name) {
    if (isGibberishName(lead.name)) {
      score -= 5;
      reasons.push("name looks like gibberish (-5)");
      spamSignals.push("name is gibberish");
    } else {
      add(10, "name provided");
    }
  }
  if (lead.product_interest) add(15, "product interest provided");
  if (lead.target_market) {
    if (isPlausibleMarket(lead.target_market)) {
      add(10, "target market provided");
    } else {
      score -= 5;
      reasons.push("target market not recognized (-5)");
      spamSignals.push("target market not a recognized market (gibberish)");
    }
  }
  if (lead.contact) add(5, "direct contact provided");
  if (lead.utm_source) add(5, "attributed traffic source");
  if (lead.catalog_touch_page || lead.catalog_touch_placement) add(10, "catalog engagement");

  if (lead.quantity) {
    const quantityNumber = Number((lead.quantity.match(/[\d,.]+/)?.[0] || "").replace(/[,\s]/g, ""));
    const quantityValid = Number.isFinite(quantityNumber) && quantityNumber >= 1 && quantityNumber <= 10_000_000;
    if (quantityValid) {
      add(15, "quantity provided");
      if (quantityNumber >= 500) add(10, "quantity at least 500");
      else if (quantityNumber >= 100) add(5, "quantity at least 100");
    } else {
      score -= 5;
      reasons.push("quantity is not a valid number (-5)");
      spamSignals.push("quantity is not a valid number (gibberish)");
    }
  }

  const messageLength = lead.message?.length || 0;
  if (messageLength >= 80) add(10, "detailed message");
  if (messageLength >= 200) add(5, "high-detail message");
  if (lead.message && /^\d{6,}$/.test(lead.message.trim())) {
    score -= 5;
    reasons.push("message is a numeric string, not text (-5)");
    spamSignals.push("message is numeric only (gibberish)");
  }

  const commercialText = [lead.company, lead.product_interest, lead.quantity, lead.target_market, lead.message]
    .filter(Boolean)
    .join(" ");
  const hasCommercialIntent = /\b(wholesale|distributor|retailer|import(?:er)?|bulk|oem|odm|private[ -]?label|brand|store|shop|order|boutique|commande|grossiste|distributeur|importateur|marque|achat|quantit[eé]|catalogue)\b/i.test(commercialText);
  if (hasCommercialIntent) {
    add(10, "commercial buying intent");
  }

  const emailDomain = lead.email?.split("@").pop()?.toLowerCase() || "";
  const freeEmailDomains = new Set([
    "gmail.com", "outlook.com", "hotmail.com", "yahoo.com", "icloud.com", "qq.com", "163.com", "126.com",
  ]);
  if (emailDomain && !freeEmailDomains.has(emailDomain)) {
    if (SUSPICIOUS_EMAIL_DOMAINS.has(emailDomain)) {
      spamSignals.push(`suspicious email domain: ${emailDomain}`);
    } else {
      add(10, "business email domain");
    }
  }

  const isSpam = spamSignals.length >= 2 || (spamSignals.length === 1 && !hasCommercialIntent && !lead.message);
  const cappedScore = Math.max(0, Math.min(score, 100));
  let priority = cappedScore >= 65 ? "HOT" : cappedScore >= 35 ? "WARM" : "COLD";
  if (isSpam) priority = "SPAM";
  return { score: cappedScore, priority, reasons, isSpam, spamReasons: spamSignals };
}

type ReplyLead = {
  name: string | null;
  company: string | null;
  submission_type: string;
  product_interest: string | null;
};

function petCustomerReplyContent(row: ReplyLead) {
  const greetingName = row.name || row.company;
  const greeting = greetingName ? `Hello ${greetingName},` : "Hello,";
  const requestSummary = row.product_interest
    ? `We have recorded your interest in: ${row.product_interest}.`
    : "We have recorded your product request.";
  const subject = row.submission_type === "catalog"
    ? "Your Entrol pet products catalog and next steps"
    : "We received your Entrol product inquiry";
  const catalogUrl = "https://www.entrol.com/assets/Entrol-Pet-Products-Catalog-2026.pdf";
  const contactUrl = "https://www.entrol.com/contact.html";
  const text = [
    greeting,
    "",
    "Thank you for contacting Entrol. Your inquiry has been received successfully, and our sales team will review it and reply within one business day.",
    requestSummary,
    "",
    `Download our 2026 pet products catalog: ${catalogUrl}`,
    "",
    "Please reply with the product codes, estimated quantities, destination country and any private-label or packaging requirements. We will then confirm current availability, MOQ, pricing, production lead time and shipping options.",
    "",
    "For small direct-ship orders, international freight can be relatively high. Bulk purchasing and consolidated shipments are usually more economical; the best option depends on the products and destination.",
    "",
    "No price, stock level, production date or freight cost is confirmed until our sales team sends a written quotation.",
    "",
    `Contact page: ${contactUrl}`,
    "Email: wangyan@entrol.com",
    "WhatsApp: +86 152 6313 0999",
    "",
    "Best regards,",
    "Entrol Sales Team",
    "Weihai Yuanchuang Import & Export Co., Ltd.",
  ].join("\n");
  const html = `<!doctype html>
<html lang="en"><body style="margin:0;background:#f4f7f9;font-family:Arial,sans-serif;color:#1f2d38">
<div style="max-width:640px;margin:0 auto;padding:28px 18px">
  <div style="background:#ffffff;border:1px solid #dde6ec;border-radius:14px;padding:30px">
    <p style="margin:0 0 18px;font-size:16px">${escapeHtml(greeting)}</p>
    <h1 style="margin:0 0 16px;color:#17324d;font-size:24px">Thank you for contacting Entrol</h1>
    <p style="margin:0 0 14px;line-height:1.65">Your inquiry has been received successfully. Our sales team will review it and reply within one business day.</p>
    <p style="margin:0 0 20px;line-height:1.65">${escapeHtml(requestSummary)}</p>
    <p style="margin:22px 0"><a href="${catalogUrl}" style="display:inline-block;padding:12px 18px;border-radius:8px;background:#246b9e;color:#ffffff;text-decoration:none;font-weight:700">Download the 2026 Pet Products Catalog</a></p>
    <p style="margin:0 0 14px;line-height:1.65">Please reply with the product codes, estimated quantities, destination country and any private-label or packaging requirements. We will then confirm current availability, MOQ, pricing, production lead time and shipping options.</p>
    <p style="margin:0 0 14px;line-height:1.65">For small direct-ship orders, international freight can be relatively high. Bulk purchasing and consolidated shipments are usually more economical; the best option depends on the products and destination.</p>
    <p style="margin:18px 0;padding:12px 14px;border-left:4px solid #d69b2d;background:#fff8e8;line-height:1.55"><strong>Quotation notice:</strong> No price, stock level, production date or freight cost is confirmed until our sales team sends a written quotation.</p>
    <p style="margin:20px 0 0;line-height:1.65">Email: <a href="mailto:wangyan@entrol.com">wangyan@entrol.com</a><br>WhatsApp: <a href="https://wa.me/8615263130999">+86 152 6313 0999</a><br><a href="${contactUrl}">Contact Entrol</a></p>
    <p style="margin:24px 0 0;line-height:1.55">Best regards,<br><strong>Entrol Sales Team</strong><br>Weihai Yuanchuang Import &amp; Export Co., Ltd.</p>
  </div>
</div>
</body></html>`;
  return { subject, text, html };
}

function senderWithDisplayName(sender: string, displayName: string): string {
  const bracketedEmail = sender.match(/<([^<>\s]+@[^<>\s]+)>/)?.[1];
  const bareEmail = sender.match(/^[^<>\s]+@[^<>\s]+$/)?.[0];
  const email = bracketedEmail || bareEmail;
  return email ? `${displayName} <${email}>` : sender;
}

function socksCustomerReplyContent(row: ReplyLead) {
  const greetingName = row.name || row.company;
  const greeting = greetingName ? `Hello ${greetingName},` : "Hello,";
  const requestSummary = row.product_interest
    ? `We have recorded your interest in: ${row.product_interest}.`
    : "We have recorded your sock sourcing request.";
  const subject = row.submission_type === "catalog"
    ? "Your Entrol Socks OEM/ODM request and next steps"
    : "We received your Entrol Socks inquiry";
  const siteUrl = "https://socks.entrol.com/";
  const contactUrl = "https://socks.entrol.com/contact.html";
  const text = [
    greeting,
    "",
    "Thank you for contacting Entrol Socks. Your inquiry has been received successfully, and our sock sourcing team will review it and reply within one business day.",
    requestSummary,
    "",
    "To prepare an accurate quotation, please reply with the sock type, material composition, size range, estimated quantity, logo or pattern requirements, packaging requirements, destination country and postal code, and required delivery date.",
    "",
    "OEM and ODM options depend on the selected construction, yarn, artwork, quantity and packaging. We will confirm the applicable MOQ, unit pricing, sample terms, production lead time and shipping options in a written quotation.",
    "",
    "No price, MOQ, sample charge, production date or freight cost is confirmed until our sock sourcing team sends a written quotation.",
    "",
    `Socks website: ${siteUrl}`,
    `Contact page: ${contactUrl}`,
    "Email: wangyan@entrol.com",
    "",
    "Best regards,",
    "Entrol Socks Team",
    "Weihai Yuanchuang Import & Export Co., Ltd.",
  ].join("\n");
  const html = `<!doctype html>
<html lang="en"><body style="margin:0;background:#f4f7f9;font-family:Arial,sans-serif;color:#1f2d38">
<div style="max-width:640px;margin:0 auto;padding:28px 18px">
  <div style="background:#ffffff;border:1px solid #dde6ec;border-radius:14px;padding:30px">
    <p style="margin:0 0 18px;font-size:16px">${escapeHtml(greeting)}</p>
    <h1 style="margin:0 0 16px;color:#17324d;font-size:24px">Thank you for contacting Entrol Socks</h1>
    <p style="margin:0 0 14px;line-height:1.65">Your inquiry has been received successfully. Our sock sourcing team will review it and reply within one business day.</p>
    <p style="margin:0 0 20px;line-height:1.65">${escapeHtml(requestSummary)}</p>
    <p style="margin:0 0 14px;line-height:1.65">To prepare an accurate quotation, please reply with the sock type, material composition, size range, estimated quantity, logo or pattern requirements, packaging requirements, destination country and postal code, and required delivery date.</p>
    <p style="margin:0 0 14px;line-height:1.65">OEM and ODM options depend on the selected construction, yarn, artwork, quantity and packaging. We will confirm the applicable MOQ, unit pricing, sample terms, production lead time and shipping options in a written quotation.</p>
    <p style="margin:18px 0;padding:12px 14px;border-left:4px solid #d69b2d;background:#fff8e8;line-height:1.55"><strong>Quotation notice:</strong> No price, MOQ, sample charge, production date or freight cost is confirmed until our sock sourcing team sends a written quotation.</p>
    <p style="margin:20px 0 0;line-height:1.65"><a href="${siteUrl}">Entrol Socks website</a><br>Email: <a href="mailto:wangyan@entrol.com">wangyan@entrol.com</a><br><a href="${contactUrl}">Contact Entrol Socks</a></p>
    <p style="margin:24px 0 0;line-height:1.55">Best regards,<br><strong>Entrol Socks Team</strong><br>Weihai Yuanchuang Import &amp; Export Co., Ltd.</p>
  </div>
</div>
</body></html>`;
  return { subject, text, html };
}

function kjadehomeCustomerReplyContent(row: ReplyLead) {
  const greetingName = row.name || row.company;
  const greeting = greetingName ? `Hello ${greetingName},` : "Hello,";
  const requestSummary = row.product_interest
    ? `We have recorded your interest in: ${row.product_interest}.`
    : "We have recorded your sourcing request.";
  const subject = "We received your KJadeHome sourcing inquiry";
  const siteUrl = "https://www.kjadehome.com/";
  const contactUrl = "https://www.kjadehome.com/inquiry.html";
  const text = [
    greeting,
    "",
    "Thank you for contacting KJadeHome. Your inquiry has been received successfully, and our sourcing team will review it and reply within one business day.",
    requestSummary,
    "",
    "To prepare a relevant quotation, please reply with the product references or photos, materials, dimensions, estimated quantities, destination country and postal code, customization requirements and required delivery date.",
    "",
    "MOQ, pricing, sample terms, production lead time and shipping options depend on the selected product and order requirements. They are not confirmed until our team sends a written quotation.",
    "",
    `Website: ${siteUrl}`,
    `Contact page: ${contactUrl}`,
    "Email: wangyan@entrol.com",
    "",
    "Best regards,",
    "KJadeHome Sourcing Team",
    "Weihai Yuanchuang Import & Export Co., Ltd.",
  ].join("\n");
  const html = `<!doctype html>
<html lang="en"><body style="margin:0;background:#f4f7f9;font-family:Arial,sans-serif;color:#1f2d38">
<div style="max-width:640px;margin:0 auto;padding:28px 18px">
  <div style="background:#ffffff;border:1px solid #dde6ec;border-radius:14px;padding:30px">
    <p style="margin:0 0 18px;font-size:16px">${escapeHtml(greeting)}</p>
    <h1 style="margin:0 0 16px;color:#0b1f3a;font-size:24px">Thank you for contacting KJadeHome</h1>
    <p style="margin:0 0 14px;line-height:1.65">Your inquiry has been received successfully. Our sourcing team will review it and reply within one business day.</p>
    <p style="margin:0 0 20px;line-height:1.65">${escapeHtml(requestSummary)}</p>
    <p style="margin:0 0 14px;line-height:1.65">To prepare a relevant quotation, please reply with the product references or photos, materials, dimensions, estimated quantities, destination country and postal code, customization requirements and required delivery date.</p>
    <p style="margin:18px 0;padding:12px 14px;border-left:4px solid #c9a86a;background:#fff8e8;line-height:1.55"><strong>Quotation notice:</strong> MOQ, pricing, sample terms, production lead time and shipping options depend on the selected product and order requirements. They are not confirmed until our team sends a written quotation.</p>
    <p style="margin:20px 0 0;line-height:1.65"><a href="${siteUrl}">KJadeHome website</a><br>Email: <a href="mailto:wangyan@entrol.com">wangyan@entrol.com</a><br><a href="${contactUrl}">Contact KJadeHome</a></p>
    <p style="margin:24px 0 0;line-height:1.55">Best regards,<br><strong>KJadeHome Sourcing Team</strong><br>Weihai Yuanchuang Import &amp; Export Co., Ltd.</p>
  </div>
</div>
</body></html>`;
  return { subject, text, html };
}

function customerReplyContent(site: SiteConfig, row: ReplyLead) {
  if (site.businessUnit === "socks") return socksCustomerReplyContent(row);
  if (site.businessUnit === "kjadehome") return kjadehomeCustomerReplyContent(row);
  return petCustomerReplyContent(row);
}

Deno.serve(async (req: Request) => {
  const origin = req.headers.get("origin");
  const site = siteForOrigin(origin);

  if (req.method === "OPTIONS") {
    if (!site) return jsonResponse(origin, { ok: false, error: "origin_not_allowed" }, 403);
    return new Response(null, { status: 204, headers: corsHeaders(origin) });
  }
  if (req.method !== "POST") return jsonResponse(origin, { ok: false, error: "method_not_allowed" }, 405);
  if (!site) return jsonResponse(origin, { ok: false, error: "origin_not_allowed" }, 403);

  const declaredLength = Number(req.headers.get("content-length") || "0");
  if (declaredLength > MAX_BODY_BYTES) return jsonResponse(origin, { ok: false, error: "payload_too_large" }, 413);

  let payload: Record<string, unknown>;
  try {
    const raw = await req.text();
    if (new TextEncoder().encode(raw).byteLength > MAX_BODY_BYTES) throw new Error("payload_too_large");
    payload = JSON.parse(raw);
    if (!payload || Array.isArray(payload) || typeof payload !== "object") throw new Error("invalid_payload");
  } catch (error) {
    const code = error instanceof Error && error.message === "payload_too_large" ? "payload_too_large" : "invalid_json";
    return jsonResponse(origin, { ok: false, error: code }, code === "payload_too_large" ? 413 : 400);
  }

  if (clean(payload.website, 200)) return jsonResponse(origin, { ok: true }, 202);

  const requestIdText = clean(payload.request_id, 36);
  if (!requestIdText || !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(requestIdText)) {
    return jsonResponse(origin, { ok: false, error: "invalid_request_id" }, 400);
  }

  const email = first(payload, ["email", "business_email"], TEXT_LIMITS.email);
  const contact = first(payload, ["contact", "phone", "whatsapp"], TEXT_LIMITS.contact);
  if (!email && !contact) return jsonResponse(origin, { ok: false, error: "contact_required" }, 422);
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return jsonResponse(origin, { ok: false, error: "invalid_email" }, 422);

  const safePayload = Object.fromEntries(
    Object.entries(payload)
      .filter(([key, value]) => !key.startsWith("_") && key !== "website" && typeof value === "string")
      .slice(0, 50)
      .map(([key, value]) => [key.slice(0, 100), clean(value, 5000)]),
  );
  const submissionType = clean(payload.submission_type, 20) === "catalog" || clean(payload.catalog_request, 10) ? "catalog" : "inquiry";

  const secretKeys = JSON.parse(Deno.env.get("SUPABASE_SECRET_KEYS") || "{}");
  const secretKey = secretKeys.default || Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  const supabaseUrl = Deno.env.get("SUPABASE_URL");
  if (!secretKey || !supabaseUrl) return jsonResponse(origin, { ok: false, error: "server_not_configured" }, 500);

  const admin = createClient(supabaseUrl, secretKey, { auth: { persistSession: false, autoRefreshToken: false } });
  const normalizedLead = {
    request_id: requestIdText,
    business_unit: site.businessUnit,
    source_site: site.sourceSite,
    submission_type: submissionType,
    name: first(payload, ["name", "first-name", "first_name"], TEXT_LIMITS.name),
    email,
    contact,
    company: first(payload, ["company", "company-name", "company_name"], TEXT_LIMITS.company),
    product_interest: first(payload, ["product_interest", "product-interest", "product", "product_type"], TEXT_LIMITS.product_interest),
    quantity: first(payload, ["quantity", "estimated_quantity"], TEXT_LIMITS.quantity),
    target_market: first(payload, ["target_market", "market"], TEXT_LIMITS.target_market),
    message: clean(payload.message, TEXT_LIMITS.message),
    source_page: clean(payload.source_page, TEXT_LIMITS.source_page),
    landing_page: clean(payload.landing_page, TEXT_LIMITS.landing_page),
    referrer: clean(payload.referrer, TEXT_LIMITS.referrer),
    utm_source: clean(payload.utm_source, TEXT_LIMITS.utm_source),
    utm_medium: clean(payload.utm_medium, TEXT_LIMITS.utm_medium),
    utm_campaign: clean(payload.utm_campaign, TEXT_LIMITS.utm_campaign),
    utm_content: clean(payload.utm_content, TEXT_LIMITS.utm_content),
    utm_term: clean(payload.utm_term, TEXT_LIMITS.utm_term),
    catalog_touch_page: clean(payload.catalog_touch_page, TEXT_LIMITS.catalog_touch_page),
    catalog_touch_placement: clean(payload.catalog_touch_placement, TEXT_LIMITS.catalog_touch_placement),
    catalog_touched_at: cleanTimestamp(payload.catalog_touched_at),
    inquiry_trigger: clean(payload.inquiry_trigger, TEXT_LIMITS.inquiry_trigger),
    user_agent: clean(req.headers.get("user-agent"), 1000),
  };
  let recentDuplicateEmail = false;
  if (email) {
    const recentCutoff = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
    const { data: recentEmailRows, error: recentEmailError } = await admin
      .from("entrol_leads")
      .select("id")
      .eq("email", email)
      .eq("business_unit", site.businessUnit)
      .gte("created_at", recentCutoff)
      .limit(1);
    if (recentEmailError) console.error("recent_email_check_failed", recentEmailError.code, recentEmailError.message);
    recentDuplicateEmail = Boolean(recentEmailRows?.length);
  }
  const abuseAssessment = assessLeadAbuse(normalizedLead, { recentDuplicateEmail });
  const leadScoring = scoreLead(normalizedLead);
  const isQuarantined = leadScoring.isSpam || abuseAssessment.quarantined;
  const scoredPayload = {
    ...safePayload,
    business_unit: site.businessUnit,
    source_site: site.sourceSite,
    origin,
    lead_score: leadScoring.score,
    lead_priority: leadScoring.priority,
    lead_score_reasons: leadScoring.reasons,
    lead_is_spam: leadScoring.isSpam,
    lead_spam_reasons: leadScoring.spamReasons,
    lead_scored_at: new Date().toISOString(),
    abuse_status: isQuarantined ? "QUARANTINE" : "PASS",
    abuse_risk_score: abuseAssessment.riskScore,
    abuse_reasons: abuseAssessment.reasons,
    abuse_checked_at: new Date().toISOString(),
    ...(isQuarantined ? { customer_auto_reply_status: "suppressed_spam" } : {}),
  };
  const row = { ...normalizedLead, raw_payload: scoredPayload };

  const { data, error } = await admin.from("entrol_leads").insert(row).select("id").single();
  if (error?.code === "23505") return jsonResponse(origin, { ok: true, duplicate: true }, 200);
  if (error) {
    console.error("lead_insert_failed", error.code, error.message);
    return jsonResponse(origin, { ok: false, error: "storage_failed" }, 500);
  }

  const resendApiKey = Deno.env.get("RESEND_API_KEY");
  const defaultNotificationTo = Deno.env.get("ENTROL_NOTIFICATION_TO") || "wangyan@entrol.com";
  const defaultNotificationFrom = Deno.env.get("ENTROL_NOTIFICATION_FROM") || "Entrol Leads <leads@updates.entrol.com>";
  const notificationTo = Deno.env.get(site.notificationToEnv) || defaultNotificationTo;
  const notificationFrom = Deno.env.get(site.notificationFromEnv)
    || (site.businessUnit === "socks"
      ? senderWithDisplayName(defaultNotificationFrom, "Entrol Socks Leads")
      : site.businessUnit === "kjadehome"
      ? senderWithDisplayName(defaultNotificationFrom, "KJadeHome Leads")
      : defaultNotificationFrom);
  const customerReplyFrom = Deno.env.get(site.customerReplyFromEnv)
    || (site.businessUnit === "socks"
      ? senderWithDisplayName(notificationFrom, "Entrol Socks Team")
      : site.businessUnit === "kjadehome"
      ? senderWithDisplayName(notificationFrom, "KJadeHome Sourcing Team")
      : notificationFrom);
  let notificationStatus = "not_configured";
  let customerReplyStatus = row.email ? "not_configured" : "not_applicable";

  if (isQuarantined) {
    notificationStatus = "not_configured";
    customerReplyStatus = "not_applicable";
    const { error: quarantineStatusError } = await admin
      .from("entrol_leads")
      .update({ notification_status: "not_configured" })
      .eq("id", data.id);
    if (quarantineStatusError) console.error("quarantine_status_update_failed", quarantineStatusError.code, quarantineStatusError.message);
  } else if (resendApiKey) {
    const subjectName = row.company || row.name || row.email || row.contact || "New lead";
    const notificationText = [
      site.notificationIntro,
      "",
      `Lead ID: ${data.id}`,
      `Business unit: ${site.businessUnit}`,
      `Source site: ${site.sourceSite}`,
      `Priority: ${leadScoring.priority}`,
      `Lead score: ${leadScoring.score}/100`,
      `Score reasons: ${leadScoring.reasons.join("; ") || "No qualifying signals"}`,
      `Spam signals: ${leadScoring.isSpam ? leadScoring.spamReasons.join("; ") : "none"}`,
      `Type: ${row.submission_type}`,
      `Name: ${row.name || "-"}`,
      `Company: ${row.company || "-"}`,
      `Email: ${row.email || "-"}`,
      `Contact: ${row.contact || "-"}`,
      `Product: ${row.product_interest || "-"}`,
      `Quantity: ${row.quantity || "-"}`,
      `Target market: ${row.target_market || "-"}`,
      `Message: ${row.message || "-"}`,
      `Source: ${row.source_page || "-"}`,
      `Landing page: ${row.landing_page || "-"}`,
      `Campaign: ${row.utm_campaign || "-"}`,
      `Catalog touch: ${row.catalog_touch_placement || "-"} | ${row.catalog_touch_page || "-"}`,
      `Catalog touched at: ${row.catalog_touched_at || "-"}`,
      `Inquiry trigger: ${row.inquiry_trigger || "-"}`,
    ].join("\n");

    try {
      const emailResponse = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${resendApiKey}` },
        body: JSON.stringify({
          from: notificationFrom,
          to: [notificationTo],
          reply_to: row.email || undefined,
          subject: `[${leadScoring.priority} ${leadScoring.score}] [${site.notificationLabel}] ${subjectName}`.slice(0, 200),
          text: notificationText,
        }),
      });
      const emailResult = await emailResponse.json().catch(() => ({}));
      notificationStatus = emailResponse.ok ? "sent" : "failed";
      await admin.from("entrol_leads").update({
        notification_status: notificationStatus,
        notification_provider: "resend",
        notification_provider_id: emailResponse.ok && typeof emailResult.id === "string" ? emailResult.id : null,
        notification_attempted_at: new Date().toISOString(),
        notification_error: emailResponse.ok ? null : String(emailResult.message || `HTTP ${emailResponse.status}`).slice(0, 1000),
      }).eq("id", data.id);
    } catch (notificationError) {
      notificationStatus = "failed";
      await admin.from("entrol_leads").update({
        notification_status: "failed",
        notification_provider: "resend",
        notification_attempted_at: new Date().toISOString(),
        notification_error: String(notificationError).slice(0, 1000),
      }).eq("id", data.id);
    }
  } else {
    await admin.from("entrol_leads").update({ notification_status: "not_configured" }).eq("id", data.id);
  }

  if (!isQuarantined && resendApiKey && row.email) {
    const replyContent = customerReplyContent(site, row);
    let customerReplyProviderId: string | null = null;
    let customerReplyError: string | null = null;
    const customerReplyAttemptedAt = new Date().toISOString();
    try {
      const customerResponse = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${resendApiKey}` },
        body: JSON.stringify({
          from: customerReplyFrom,
          to: [row.email],
          reply_to: notificationTo,
          subject: replyContent.subject,
          text: replyContent.text,
          html: replyContent.html,
        }),
      });
      const customerResult = await customerResponse.json().catch(() => ({}));
      customerReplyStatus = customerResponse.ok ? "sent" : "failed";
      customerReplyProviderId = customerResponse.ok && typeof customerResult.id === "string" ? customerResult.id : null;
      customerReplyError = customerResponse.ok ? null : String(customerResult.message || `HTTP ${customerResponse.status}`).slice(0, 500);
    } catch (customerError) {
      customerReplyStatus = "failed";
      customerReplyError = String(customerError).slice(0, 500);
    }

    await admin.from("entrol_leads").update({
      raw_payload: {
        ...scoredPayload,
        customer_auto_reply_status: customerReplyStatus,
        customer_auto_reply_provider: "resend",
        customer_auto_reply_provider_id: customerReplyProviderId,
        customer_auto_reply_attempted_at: customerReplyAttemptedAt,
        customer_auto_reply_error: customerReplyError,
      },
    }).eq("id", data.id);
  }

  return jsonResponse(origin, {
    ok: true,
    lead_id: data.id,
    duplicate: false,
    is_spam: isQuarantined,
    notification_status: notificationStatus,
    customer_reply_status: customerReplyStatus,
    lead_priority: leadScoring.priority,
    lead_score: leadScoring.score,
    business_unit: site.businessUnit,
  }, 201);
});
