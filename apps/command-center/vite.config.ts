import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

declare const process: {
  readonly env: Readonly<Record<string, string | undefined>>;
};

const gailOsApiTarget =
  process.env.GAIL_OS_API_PROXY_TARGET ?? "http://127.0.0.1:8123";
const gailOsApiKey = process.env.GAIL_OS_API_KEY ?? "";
const gailOsProxy = {
  "/gail-os-api": {
    target: gailOsApiTarget,
    changeOrigin: true,
    secure: false,
    rewrite: (path: string) => path.replace(/^\/gail-os-api/, "/api/v1"),
    headers: gailOsApiKey ? { "X-Api-Key": gailOsApiKey } : {},
  },
};

export default defineConfig({
  plugins: [react()],
  define: {
    "import.meta.env.VITE_GAIL_OS_PROXY_HAS_API_KEY": JSON.stringify(
      gailOsApiKey ? "true" : "false",
    ),
  },
  server: {
    proxy: gailOsProxy,
  },
  preview: {
    proxy: gailOsProxy,
  },
});
