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
  experimental: {
    turbo: {
      resolveAlias: {
        "react-native": "react-native-web",
      },
    },
  },
  // webpack config removed per instructions
  // rewrites removed per instructions
};
