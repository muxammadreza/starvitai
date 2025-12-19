module.exports = {
  reactStrictMode: true,
  transpilePackages: ["react-native-web", "@starvit/ui"],
  turbopack: {
    resolveAlias: {
      "react-native": "react-native-web",
    },
  },
  experimental: {
  },
  webpack: (config) => {
    config.resolve.alias = {
      ...(config.resolve.alias || {}),
      "react-native$": "react-native-web",
    };
    config.resolve.extensions = [
      ".web.js",
      ".web.jsx",
      ".web.ts",
      ".web.tsx",
      ...config.resolve.extensions,
    ];
    return config;
  },
};
