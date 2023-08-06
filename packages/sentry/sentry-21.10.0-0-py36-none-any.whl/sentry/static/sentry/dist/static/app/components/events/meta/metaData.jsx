Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isNil_1 = (0, tslib_1.__importDefault)(require("lodash/isNil"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
/**
 * Retrieves metadata from an object (object should be a proxy that
 * has been decorated using `app/components/events/meta/metaProxy/withMeta`
 */
const MetaData = ({ children, object, prop, required, }) => {
    const value = object[prop];
    const meta = (0, metaProxy_1.getMeta)(object, prop);
    if (required && (0, isNil_1.default)(value) && !meta) {
        return null;
    }
    return <errorBoundary_1.default mini>{children(value, meta)}</errorBoundary_1.default>;
};
exports.default = MetaData;
//# sourceMappingURL=metaData.jsx.map