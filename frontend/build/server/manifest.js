const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["css/globals.css","favicon.png","images/foodlyze-high-resolution-logo.png"]),
	mimeTypes: {".css":"text/css",".png":"image/png"},
	_: {
		client: {start:"_app/immutable/entry/start.DSodupeD.js",app:"_app/immutable/entry/app.UwfTVaAY.js",imports:["_app/immutable/entry/start.DSodupeD.js","_app/immutable/chunks/VqLEZLB1.js","_app/immutable/chunks/B9CUAD_v.js","_app/immutable/chunks/CFzP_YVO.js","_app/immutable/entry/app.UwfTVaAY.js","_app/immutable/chunks/B9CUAD_v.js","_app/immutable/chunks/VD4A6Zb7.js","_app/immutable/chunks/DH8YWvmg.js","_app/immutable/chunks/d_3EPzzW.js","_app/immutable/chunks/CFzP_YVO.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./chunks/0-1SwmpFhn.js')),
			__memo(() => import('./chunks/1-BmVJtNNo.js')),
			__memo(() => import('./chunks/2-i-t84RUo.js'))
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
