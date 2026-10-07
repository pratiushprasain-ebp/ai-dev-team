# <Project name>

<!-- Project brief for Claude Code and the team agents. Keep it under ~150 lines; link to docs instead of copying them. -->

## Product

<One paragraph: who it's for and what problem it solves.>

- PRD: docs/product/PRD.md · Backlog: docs/product/backlog.md
- Client: <name> · Milestones: <dates> · Compliance: <e.g. GDPR / Australian Privacy Act / none>

## Stack (decisions and reasons live in docs/adr/)

- Website + web app: <Next.js version, router, styling, UI kit, CMS if any>
- Mobile: <Expo SDK, React Native, Expo Router, EAS>
- API: <where it runs, framework, contract style>
- Database: <Postgres provider, ORM>
- Auth: <library or provider>
- Hosting and CI: <e.g. Vercel, GitHub Actions>
- Monitoring: <e.g. Sentry, uptime checks>

## Repo layout

```
apps/web         # Next.js: website + web app
apps/mobile      # Expo app
packages/shared  # Zod schemas, types, API client (single source of truth for contracts)
packages/tokens  # design tokens for web and mobile
packages/config  # tsconfig, ESLint, Prettier presets
docs/            # product, architecture, adr, design, ux, qa, runbooks
```

## Commands

- Install: `pnpm install`
- Dev: `pnpm dev` (web) · `pnpm --filter mobile start` (mobile)
- Lint / typecheck: `pnpm lint` · `pnpm typecheck`
- Tests: `pnpm test` (unit) · `pnpm test:integration` · `pnpm test:e2e` (web) · `maestro test apps/mobile/.maestro` (mobile)
- Build: `pnpm build`
- Database (local only): `pnpm db:generate` · `pnpm db:migrate`

## Conventions

- TypeScript strict. API types come from `packages/shared`; never redefine them in an app.
- API: <REST + OpenAPI / ...>, error envelope `{ error: { code, message, details?, requestId } }`, cursor pagination.
- Styling: tokens only (`packages/tokens`); no hard-coded colors or spacing.
- Naming: <files kebab-case, components PascalCase, hooks useX, ...>
- Git: <branch naming>, Conventional Commits (`feat(scope): …`, `fix(scope): …`).
- <Project-specific rules>

## Environments

- local · preview (per PR) · staging · production. Details: docs/runbooks/environments.md
- Every env var is documented in `.env.example`. Never commit `.env` files or secrets.

## Team workflow

- `/team-feature <story>` · `/team-bugfix <bug>` · `/team-review` · `/team-release <version>` · `/team-estimate` · `/team-kickoff`
- Agents read `docs/` before acting and record their output there. Definition of Done, handoff format, and safety rules: the `team-standards` skill.

## Known gotchas

<!-- Append as discovered: symptom → cause → fix. -->
