# CLAUDE.md — Next.js 15 + SQLite SaaS Project

## Stack & Versions
- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript 5.7+
- **Database:** better-sqlite3 (local dev) / Turso (production)
- **ORM:** Drizzle ORM
- **Auth:** NextAuth.js v5 (Auth.js)
- **Styling:** Tailwind CSS v4
- **Validation:** Zod
- **Payments:** Stripe

## Project Structure
```
src/
  app/           # Next.js App Router pages
  components/    # Shared React components
  lib/           # Utilities, db client, auth helpers
  db/
    schema.ts    # Drizzle schema definitions
    migrations/  # Auto-generated SQL migrations
  actions/       # Server Actions (use 'use server')
  hooks/         # Client-side React hooks
```

## Database Conventions
- ALL schema changes go through `src/db/schema.ts`
- Run `npm run db:generate` after schema changes, then `npm run db:migrate`
- Use Drizzle's relational queries (`db.query.xxx`) for joins
- NEVER write raw SQL unless it's a migration
- Timestamps: every table has `createdAt` and `updatedAt`

## Component Patterns
- Server Components by default, Client Components only when needed
- Use `'use client'` only for: event handlers, hooks, browser APIs
- Data fetching: Server Components fetch directly, no API routes for internal data
- Forms: React Server Actions with Zod validation
- Loading states: Use React Suspense boundaries

## Dev Commands
```bash
npm run dev          # Start dev server
npm run db:studio    # Open Drizzle Studio
npm run db:generate  # Generate migrations
npm run db:migrate   # Apply migrations
npm run lint         # ESLint
npm run typecheck    # TypeScript check
npm run test         # Vitest
```

## What We DON'T Do
- No API routes for internal data (use Server Components / Actions)
- No `any` types — always derive from Zod schemas
- No relative imports beyond 3 levels (use @/ aliases)
- No client-side data fetching (use Server Components)
- No `useEffect` for data (use Server Components or React Query only for client mutations)
