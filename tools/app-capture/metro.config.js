const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');
const config = getDefaultConfig(__dirname);
const S = (f) => path.join(__dirname, 'web-stubs', f);
const map = {
  'react-native-google-mobile-ads': S('ads.js'),
  'react-native-purchases': S('purchases.js'),
  'expo-notifications': S('notifications.js'),
  'expo-tracking-transparency': S('misc.js'),
  'expo-store-review': S('misc.js'),
  'expo-apple-authentication': S('misc.js'),
  'expo-image-picker': S('misc.js'),
  '@bacons/apple-targets': S('misc.js'),
};
config.resolver.resolveRequest = (ctx, name, platform) => {
  if (platform === 'web' && map[name]) return { type: 'sourceFile', filePath: map[name] };
  return ctx.resolveRequest(ctx, name, platform);
};
module.exports = config;
