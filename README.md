# STADIUMAI

The AI-Powered Smart Stadium Assistant for FIFA World Cup 2026.

STADIUMAI is a GenAI-enabled stadium operations platform for fans, volunteers, organizers, and admins. It combines RAG, live operational data, WebSockets, role dashboards, accessibility controls, multilingual assistance, crowd intelligence, emergency copilot workflows, transportation guidance, and sustainability analytics.

## Stack

- Frontend: React 19, TypeScript, Vite, Tailwind CSS, Shadcn-style reusable UI, React Router, React Query, Framer Motion, Leaflet, Recharts
- Backend: Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL/Supabase-ready
- AI: OpenAI-ready service boundary, LangChain/FAISS dependencies, RAG prompt assets, conversation audit persistence
- Auth: JWT, bcrypt, RBAC, Google OAuth integration point
- Realtime: WebSockets
- Deployment: Docker, Docker Compose, GitHub Actions, Vercel, Railway

## Run

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Frontend: `http://localhost:5173`
Backend: `http://localhost:8000`
Swagger: `http://localhost:8000/docs`

## Local Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Security

The backend includes JWT auth, bcrypt password hashing, RBAC dependencies, secure response headers, CORS configuration, typed validation, ORM query construction, environment-based secrets, and HTTPS-ready session settings. Put production secrets in Railway/Supabase/Vercel secret stores, not in source control.

## Feature Coverage

- Landing page with animated FIFA-style hero, stats, AI intro, features, testimonials, FAQ, contact, footer, and dark mode
- Register, login, forgot password flow, JWT sessions, role-based access hooks, Google OAuth integration point
- Fan dashboard: matches, tickets, seat finder, parking, food, navigation, crowd, alerts, AI chat, language, voice UI
- Volunteer dashboard: zone, tasks, crowd alerts, emergency notifications, incident reporting flow, AI assistant, shift info
- Organizer dashboard: crowd analytics, queue length, heat map, incidents, volunteers, transport, food, energy, water, waste, carbon, AI recommendations
- Admin dashboard: user, stadium, volunteer, match, ticket, gate, analytics, and audit surfaces
- AI assistant answers from retrieved live tables and persists conversation sources
- Emergency copilot generates summary, priority, nearest team, recommended actions, and evacuation guidance
- Accessibility: keyboard focus, ARIA labels, high contrast toggle, adjustable font mode, accessible route data model

## Testing

```powershell
pytest
cd frontend
npm test
```

Node/npm are required for frontend tests and builds. The current shell used to generate this project did not have Node/npm installed.

## GitHub Repository Setup

This project is hosted on GitHub as a public repository. To clone and contribute:

```bash
git clone https://github.com/YOUR_USERNAME/StadiumAI.git
cd StadiumAI
```

### For Developers

1. **Fork the repository** (if you want to contribute)
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/StadiumAI.git
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and commit:
   ```bash
   git commit -m "Add your feature description"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request** on the main repository

## Contributing

We welcome contributions! Please follow these guidelines:

- **Code Style**: 
  - Backend: Follow PEP 8 (use `ruff` for linting)
  - Frontend: Use ESLint configuration provided
- **Testing**: Ensure tests pass before submitting PRs
- **Documentation**: Update README and docstrings for new features
- **Commits**: Use clear, descriptive commit messages
- **Issues**: Check existing issues before creating new ones

## License

This project is open source. See LICENSE file for details.

## Project Status

🚀 **Active Development** - StadiumAI is under active development for FIFA World Cup 2026.

## Support & Contact

- **Issues**: Report bugs or request features via GitHub Issues
- **Email**: admin@stadiumai.example
- **Documentation**: See `GITHUB_SETUP.md` for repository setup instructions

## Acknowledgments

Built with modern web technologies for safer, faster, and more sustainable stadium operations during major sporting events.

---

**Last Updated**: 2026-07-14
**Version**: 1.0.0
