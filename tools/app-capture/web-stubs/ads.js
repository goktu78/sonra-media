const noop = () => {};
const p = (v) => Promise.resolve(v);
const ad = { load: noop, show: () => p(), addAdEventListener: () => noop, loaded: false };
module.exports = {
  __esModule: true,
  default: () => ({ initialize: () => p([]), setRequestConfiguration: () => p() }),
  AdEventType: { LOADED: 'loaded', CLOSED: 'closed', ERROR: 'error' },
  AdsConsent: { requestInfoUpdate: () => p({}), loadAndShowConsentFormIfRequired: () => p({}), gatherConsent: () => p({}), getConsentInfo: () => p({ canRequestAds: true }) },
  BannerAd: () => null,
  BannerAdSize: { ANCHORED_ADAPTIVE_BANNER: 'a', BANNER: 'b' },
  InterstitialAd: { createForAdRequest: () => ad },
  TestIds: { BANNER: 'x', INTERSTITIAL: 'y' },
};
