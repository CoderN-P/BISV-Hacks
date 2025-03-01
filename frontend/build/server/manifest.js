const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["css/globals.css","favicon.png"]),
	mimeTypes: {".css":"text/css",".png":"image/png"},
	_: {
		client: {start:"_app/immutable/entry/start.D2MuPijb.js",app:"_app/immutable/entry/app.DB_Ecm1c.js",imports:["_app/immutable/entry/start.D2MuPijb.js","_app/immutable/chunks/Cl5VadBT.js","_app/immutable/chunks/C_2bOysV.js","_app/immutable/chunks/BDLwdBMC.js","_app/immutable/entry/app.DB_Ecm1c.js","_app/immutable/chunks/C_2bOysV.js","_app/immutable/chunks/DasDVUsj.js","_app/immutable/chunks/Dtw3Ef1T.js","_app/immutable/chunks/CAApebIF.js","_app/immutable/chunks/BDLwdBMC.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./chunks/0-Bw7Go1yu.js')),
			__memo(() => import('./chunks/1-CGlP_sqn.js')),
			__memo(() => import('./chunks/2-CP1nj_U0.js'))
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
