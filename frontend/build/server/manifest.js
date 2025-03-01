const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["favicon.png","images/android-chrome-192x192.png","images/android-chrome-512x512.png","images/apple-touch-icon.png","images/favicon-16x16.png","images/favicon-32x32.png","images/favicon.ico","images/foodlyze-high-resolution-logo.png"]),
	mimeTypes: {".png":"image/png"},
	_: {
		client: {start:"_app/immutable/entry/start.BmsksOli.js",app:"_app/immutable/entry/app.D9CQQnFB.js",imports:["_app/immutable/entry/start.BmsksOli.js","_app/immutable/chunks/ModyhvZS.js","_app/immutable/chunks/DSwFemxF.js","_app/immutable/chunks/DSAqiy82.js","_app/immutable/entry/app.D9CQQnFB.js","_app/immutable/chunks/DSwFemxF.js","_app/immutable/chunks/CcviYXUN.js","_app/immutable/chunks/a2Wh04Ca.js","_app/immutable/chunks/DJ1xygrn.js","_app/immutable/chunks/DSAqiy82.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./chunks/0-C7Dog5rC.js')),
			__memo(() => import('./chunks/1-Asm720MV.js')),
			__memo(() => import('./chunks/2-CNOBHM-X.js'))
		],
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
