const p = (v) => Promise.resolve(v);
module.exports = { __esModule: true,
  getTrackingPermissionsAsync: () => p({ granted: false, status: 'denied' }), requestTrackingPermissionsAsync: () => p({ granted: false, status: 'denied' }),
  isAvailableAsync: () => p(false), hasAction: () => p(false), requestReview: () => p(),
  signInAsync: () => Promise.reject(new Error('web')), AppleAuthenticationScope: { FULL_NAME: 0, EMAIL: 1 },
  AppleAuthenticationButton: () => null, AppleAuthenticationButtonType: {}, AppleAuthenticationButtonStyle: {},
  launchImageLibraryAsync: () => p({ canceled: true }), requestMediaLibraryPermissionsAsync: () => p({ granted: false }), MediaTypeOptions: {},
  ExtensionStorage: class { set(){} get(){ return null; } remove(){} static reloadWidget(){} },
};
