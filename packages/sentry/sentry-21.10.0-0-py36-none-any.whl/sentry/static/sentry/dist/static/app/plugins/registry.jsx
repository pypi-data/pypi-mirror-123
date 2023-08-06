Object.defineProperty(exports, "__esModule", { value: true });
/* eslint no-console:0 */
const defaultIssuePlugin_1 = require("app/plugins/defaultIssuePlugin");
const defaultPlugin_1 = require("app/plugins/defaultPlugin");
const utils_1 = require("app/utils");
class Registry {
    constructor() {
        this.plugins = {};
        this.assetCache = {};
    }
    isLoaded(data) {
        return (0, utils_1.defined)(this.plugins[data.id]);
    }
    load(data, callback) {
        let remainingAssets = data.assets.length;
        // TODO(dcramer): we should probably register all valid plugins
        const finishLoad = () => {
            if (!(0, utils_1.defined)(this.plugins[data.id])) {
                if (data.type === 'issue-tracking') {
                    this.plugins[data.id] = defaultIssuePlugin_1.DefaultIssuePlugin;
                }
                else {
                    this.plugins[data.id] = defaultPlugin_1.DefaultPlugin;
                }
            }
            console.info('[plugins] Loaded ' + data.id + ' as {' + this.plugins[data.id].name + '}');
            callback(this.get(data));
        };
        if (remainingAssets === 0) {
            finishLoad();
            return;
        }
        const onAssetLoaded = function () {
            remainingAssets--;
            if (remainingAssets === 0) {
                finishLoad();
            }
        };
        const onAssetFailed = function (asset) {
            remainingAssets--;
            console.error('[plugins] Failed to load asset ' + asset.url);
            if (remainingAssets === 0) {
                finishLoad();
            }
        };
        // TODO(dcramer): what do we do on failed asset loading?
        data.assets.forEach(asset => {
            if (!(0, utils_1.defined)(this.assetCache[asset.url])) {
                console.info('[plugins] Loading asset for ' + data.id + ': ' + asset.url);
                const s = document.createElement('script');
                s.src = asset.url;
                s.onload = onAssetLoaded.bind(this);
                s.onerror = onAssetFailed.bind(this, asset);
                s.async = true;
                document.body.appendChild(s);
                this.assetCache[asset.url] = s;
            }
            else {
                onAssetLoaded();
            }
        });
    }
    get(data) {
        const cls = this.plugins[data.id];
        if (!(0, utils_1.defined)(cls)) {
            throw new Error('Attempted to ``get`` an unloaded plugin: ' + data.id);
        }
        return new cls(data);
    }
    add(id, cls) {
        this.plugins[id] = cls;
    }
}
exports.default = Registry;
//# sourceMappingURL=registry.jsx.map