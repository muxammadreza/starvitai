module.exports = {
  reactStrictMode: true,
  transpilePackages: ["react-native-web", "@starvit/ui"],
  turbopack: {
    resolveAlias: {
      "react-native": "react-native-web",
    },
    resolveExtensions: [
      ".web.tsx",
      ".web.ts",
      ".web.jsx",
      ".web.js",
      ".tsx",
      ".ts",
      ".jsx",
      ".js",
    ],
  },
  webpack: (config) => {
    config.resolve.alias = {
      ...(config.resolve.alias || {}),
      "react-native$": "react-native-web",
    };
    return config;
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.STARVIT_API_INTERNAL_URL || "http://localhost:8000"}/api/:path*`,
      },
    ];
  },
};
