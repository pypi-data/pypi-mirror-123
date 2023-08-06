Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
// TODO(Priscila): Remove BR tags
// mapUrl not always present; e.g. uploaded source maps
const OriginalSourceInfo = ({ mapUrl, map }) => {
    if (!(0, utils_1.defined)(map) && !(0, utils_1.defined)(mapUrl)) {
        return null;
    }
    return (<react_1.Fragment>
      <strong>{(0, locale_1.t)('Source Map')}</strong>
      <br />
      {mapUrl !== null && mapUrl !== void 0 ? mapUrl : map}
      <br />
    </react_1.Fragment>);
};
exports.default = OriginalSourceInfo;
//# sourceMappingURL=originalSourceInfo.jsx.map