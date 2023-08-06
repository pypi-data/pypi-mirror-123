Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const PreviewFeature = ({ type = 'info' }) => (<alert_1.default type={type} icon={<icons_1.IconLab size="sm"/>}>
    {(0, locale_1.t)('This feature is a preview and may change in the future. Thanks for being an early adopter!')}
  </alert_1.default>);
exports.default = PreviewFeature;
//# sourceMappingURL=previewFeature.jsx.map