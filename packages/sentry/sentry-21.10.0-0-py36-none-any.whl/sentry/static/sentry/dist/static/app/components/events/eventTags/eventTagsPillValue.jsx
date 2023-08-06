Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const deviceName_1 = (0, tslib_1.__importDefault)(require("app/components/deviceName"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const utils_1 = require("app/utils");
const EventTagsPillValue = ({ tag: { key, value }, meta, isRelease, streamPath, locationSearch, }) => {
    var _a;
    const getContent = () => isRelease ? (<version_1.default version={String(value)} anchor={false} tooltipRawVersion truncate/>) : (<annotatedText_1.default value={(0, utils_1.defined)(value) && <deviceName_1.default value={String(value)}/>} meta={meta}/>);
    const content = getContent();
    if (!((_a = meta === null || meta === void 0 ? void 0 : meta.err) === null || _a === void 0 ? void 0 : _a.length) && (0, utils_1.defined)(key)) {
        return <link_1.default to={{ pathname: streamPath, search: locationSearch }}>{content}</link_1.default>;
    }
    return content;
};
exports.default = EventTagsPillValue;
//# sourceMappingURL=eventTagsPillValue.jsx.map