Object.defineProperty(exports, "__esModule", { value: true });
exports.getMeta = exports.withMeta = exports.MetaProxy = void 0;
const tslib_1 = require("tslib");
const isEmpty_1 = (0, tslib_1.__importDefault)(require("lodash/isEmpty"));
const isNull_1 = (0, tslib_1.__importDefault)(require("lodash/isNull"));
const GET_META = Symbol('GET_META');
const IS_PROXY = Symbol('IS_PROXY');
function isAnnotated(meta) {
    if ((0, isEmpty_1.default)(meta)) {
        return false;
    }
    return !(0, isEmpty_1.default)(meta.rem) || !(0, isEmpty_1.default)(meta.err);
}
class MetaProxy {
    constructor(local) {
        this.local = local;
    }
    get(obj, prop, receiver) {
        // trap calls to `getMeta` to return meta object
        if (prop === GET_META) {
            return key => {
                if (this.local && this.local[key] && this.local[key]['']) {
                    // TODO: Error checks
                    const meta = this.local[key][''];
                    return isAnnotated(meta) ? meta : undefined;
                }
                return undefined;
            };
        }
        // this is how  we can determine if current `obj` is a proxy
        if (prop === IS_PROXY) {
            return true;
        }
        const value = Reflect.get(obj, prop, receiver);
        if (!Reflect.has(obj, prop) || typeof value !== 'object' || (0, isNull_1.default)(value)) {
            return value;
        }
        // This is so we don't create a new Proxy from an object that is
        // already a proxy. Otherwise we can get into very deep recursive calls
        if (Reflect.get(obj, IS_PROXY, receiver)) {
            return value;
        }
        // Make sure we apply proxy to all children (objects and arrays)
        // Do we need to check for annotated inside of objects?
        return new Proxy(value, new MetaProxy(this.local && this.local[prop]));
    }
}
exports.MetaProxy = MetaProxy;
function withMeta(event) {
    if (!event) {
        return event;
    }
    // Return unproxied `event` if browser does not support `Proxy`
    if (typeof window.Proxy === 'undefined' || typeof window.Reflect === 'undefined') {
        return event;
    }
    // withMeta returns a type that is supposed to be 100% compatible with its
    // input type. Proxy typing on typescript is not really functional enough to
    // make this work without casting.
    //
    // https://github.com/microsoft/TypeScript/issues/20846
    return new Proxy(event, new MetaProxy(event._meta));
}
exports.withMeta = withMeta;
function getMeta(obj, prop) {
    if (!obj || typeof obj[GET_META] !== 'function') {
        return undefined;
    }
    return obj[GET_META](prop);
}
exports.getMeta = getMeta;
//# sourceMappingURL=metaProxy.jsx.map