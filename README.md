[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/deeptutor?utm_medium=integration&utm_source=button&utm_campaign=deeptutor)

# Deploy and Host DeepTutor on Railway

DeepTutor is an open-source, Apache-2.0 personal AI tutor from the HKU Data Intelligence Lab (HKUDS). Upload your documents into knowledge bases, then chat with them, get step-by-step problem solving, generate practice questions, run deep research and keep notebooks, using the LLM and embedding provider of your choice.

## About Hosting DeepTutor

This template runs the official DeepTutor 1.7.3 image (`ghcr.io/hkuds/deeptutor`, pinned by digest) as one service built from this GitHub repo. The Next.js web UI and the FastAPI backend run in the same container. The UI listens on Railway's `PORT` and proxies the API internally. Everything DeepTutor stores (settings, model keys, knowledge bases, chat history, users) lives on a volume at `/app/data`, so it survives redeploys and restarts. Login is turned on at first boot: the admin user is `admin`, and the password is generated for you in `ADMIN_PASSWORD`. After deploy, open the URL, log in, and add your LLM and embedding provider keys under Settings.

## Common Use Cases

* Study from your own PDFs, notes and textbooks with answers grounded in your documents
* Generate practice questions and quizzes, and work through problems step by step
* Run a shared tutor for a family, class or study group, with one account per learner

## Dependencies for DeepTutor Hosting

* An API key for an LLM provider (OpenAI, Anthropic, Gemini, DeepSeek, OpenRouter, a self-hosted Ollama or any OpenAI-compatible endpoint), entered in Settings after deploy
* An embedding model (the same provider usually works) for knowledge bases

### Deployment Dependencies

* [DeepTutor on GitHub](https://github.com/HKUDS/DeepTutor)
* [DeepTutor Docker image](https://github.com/HKUDS/DeepTutor/pkgs/container/deeptutor)
* [Template source repo](https://github.com/aalfath/deeptutor-railway-template)

### Implementation Details

Variables:

| Variable | Default | Purpose |
|---|---|---|
| `ADMIN_USERNAME` | `admin` | Login name of the admin account |
| `ADMIN_PASSWORD` | generated, 24 characters | Admin password; change it here and redeploy to rotate it |
| `PORT` | `3782` | Port of the web UI |

DeepTutor reads its settings from JSON files on the volume, not from environment variables. A small start script in this repo writes the login (`auth.json`, bcrypt hash only) and the port and CORS origin (`system.json`) on every boot, then starts the image's own entrypoint. Model providers, API keys and everything else are set in the web UI and kept on the volume.

The health check is `/api/auth/status`. The first deploy takes a few minutes, because the image is about 1 GB.

Admins can add more accounts under Settings → Users. Self-registration stays closed.

Updates: this template builds from [aalfath/deeptutor-railway-template](https://github.com/aalfath/deeptutor-railway-template). When we move it to a new DeepTutor release, Railway shows an "update available" notice on your project, and you choose when to apply it. Read `CHANGELOG.md` first: breaking changes are listed at the top of each entry.

## Why Deploy DeepTutor on Railway?

<!-- Recommended: Keep this section as shown below -->
Railway is a singular platform to deploy your infrastructure stack. Railway will host your infrastructure so you don't have to deal with configuration, while allowing you to vertically and horizontally scale it.

By deploying DeepTutor on Railway, you are one step closer to supporting a complete full-stack application with minimal burden. Host your servers, databases, AI agents, and more on Railway.
<!-- End recommended section -->
