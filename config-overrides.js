module.exports = function override(config, env) {
    // Add a fallback for the url module
    config.resolve.fallback = {
      "url": require.resolve("url/")
    };
  
    return config;
  };
  