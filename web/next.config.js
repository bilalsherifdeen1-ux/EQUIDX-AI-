/** @type {import('next').NextConfig} */
const isGitHubPages = process.env.GITHUB_PAGES === "true";

const nextConfig = {
  reactStrictMode: true,
  output: isGitHubPages ? "export" : "standalone",
  trailingSlash: isGitHubPages,
  ...(isGitHubPages
    ? {
        basePath: "/EQUIDX-AI-",
        assetPrefix: "/EQUIDX-AI-/",
        images: { unoptimized: true },
      }
    : {}),
};

module.exports = nextConfig;
