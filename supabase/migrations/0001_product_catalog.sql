-- Product catalogue for fishing.entrol.com
--
-- Single source of truth for every SKU the configurator, the category pages
-- and the compatibility engine are allowed to quote. Two commercial paths
-- share one catalogue:
--   * oem    — bulk private-label programs (rod MOQ 300, kits 500/1000)
--   * custom — one-off / small-batch custom builds for individual anglers
-- Each row therefore carries its own moq and price per path.
--
-- Prices are deliberately nullable: nothing goes on the site that has not
-- been confirmed by the supplying line. An empty price renders as
-- "quoted per build", never as a made-up number.

create extension if not exists "pgcrypto";

create table if not exists public.products (
  id              uuid primary key default gen_random_uuid(),
  sku             text not null unique,
  model           text,
  category        text not null check (category in ('rod', 'line', 'lure', 'reel', 'accessory')),
  subcategory     text not null,
  name            text not null,
  brand_mode      text not null default 'neutral'
                    check (brand_mode in ('neutral', 'customer', 'house')),
  specs           jsonb not null default '{}'::jsonb,
  image           text,
  moq_oem         integer,
  moq_custom      integer,
  price_oem_usd   numeric(10, 2),
  price_custom_usd numeric(10, 2),
  lead_time_oem_days    integer,
  lead_time_custom_days integer,
  unit            text not null default 'pcs',
  paths           text[] not null default array['oem', 'custom'],
  status          text not null default 'draft'
                    check (status in ('draft', 'active', 'archived')),
  source          text,
  notes           text,
  sort_order      integer not null default 0,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

create index if not exists products_category_idx on public.products (category, subcategory);
create index if not exists products_status_idx on public.products (status);
create index if not exists products_sort_idx on public.products (sort_order, sku);

-- Specs are queried by key (length, power, pe, weight_g ...) — GIN keeps
-- attribute lookups cheap as the catalogue grows.
create index if not exists products_specs_idx on public.products using gin (specs);

create or replace function public.products_touch()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

drop trigger if exists products_touch on public.products;
create trigger products_touch before update on public.products
  for each row execute function public.products_touch();

alter table public.products enable row level security;

-- The public site reads active rows only. Writes happen through the service
-- role in the dashboard / sync script, never from the browser.
drop policy if exists products_public_read on public.products;
create policy products_public_read on public.products
  for select using (status = 'active');
