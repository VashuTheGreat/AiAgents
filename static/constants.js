/* ============================================================
   constants.js  –  single source of truth for all API routes
                    and shared auth helpers.
   Loaded by base.html on every page AFTER window.APP_USER_ID
   is injected from the server.
   ============================================================ */

// ── Auth ──────────────────────────────────────────────────
/**
 * Returns the app user_id injected by the server.
 * Falls back to a session-scoped UUID if somehow not set.
 */
function getUserId() {
  if (window.APP_USER_ID && window.APP_USER_ID !== "None" && window.APP_USER_ID !== "") {
    return window.APP_USER_ID;
  }
  // Fallback: persist a random UUID for the session
  let id = sessionStorage.getItem("app_user_id");
  if (!id) {
    id = crypto.randomUUID();
    sessionStorage.setItem("app_user_id", id);
  }
  return id;
}

/**
 * Default headers to attach to every authenticated request.
 * Usage:  await fetch(ROUTES.X, { headers: AUTH_HEADERS() })
 *         await fetch(ROUTES.X, { method:"POST", headers: AUTH_HEADERS({ Accept:"application/json" }), body:... })
 */
function AUTH_HEADERS(extra = {}) {
  const headers = {
    "user_id": getUserId(),
    "Content-Type": "application/json",
    ...extra,
  };
  
  if (window.currentThreadId) {
    headers["thread_id"] = window.currentThreadId;
  }
  
  return headers;
}

// ── API Routes ────────────────────────────────────────────
const ROUTES = {
  // ── Page routes (navigation) ──────────────────────────
  HOME:    "/",
  CHAT:    "/chat",
  WEB:     "/web",
  BLOG:    "/blog",

  // ── MultiRAG / Chat ───────────────────────────────────
  CHAT_MESSAGE:  (message) => `/api/v1/chat/chat?message=${encodeURIComponent(message)}`,
  UPLOAD_FILE:   "/api/v1/uploader/",
  UPLOAD_URL:    (url) => `/api/v1/uploader/upload_url?url=${encodeURIComponent(url)}`,
  GET_FILE_FORMATS: "/api/v1/file_formats/",

  // ── Threads ───────────────────────────────────────────
  GET_ALL_THREADS: "/api/v1/thread/get_all_thread",
  LOAD_CONVERSATION: (threadId) => `/api/v1/conversation/load_conversation?thread_id=${encodeURIComponent(threadId)}`,
  DELETE_THREAD: (threadId) => `/api/v1/thread/delete_thread?thread_id=${encodeURIComponent(threadId)}`,

  // ── Web Summarizer ────────────────────────────────────
  WEB_SUMMARIZE: (url) => `/web/web_summerizer?url=${encodeURIComponent(url)}`,

  // ── Blog ──────────────────────────────────────────────
  BLOGS_LIST:     "/blog/blogs",
  BLOG_GET:       (title) => `/blog/blog/${encodeURIComponent(title)}`,
  BLOG_DELETE:    "/blog/delete_blog",
  BLOG_DOWNLOAD:  (title) => `/blog/download_blog/${encodeURIComponent(title)}`,
  BLOG_WS:        () => {
    const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
    return `${proto}//${window.location.host}/blog/ws/generate_blog`;
  },
};
