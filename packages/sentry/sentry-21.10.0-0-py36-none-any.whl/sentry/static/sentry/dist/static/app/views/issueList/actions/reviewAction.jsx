Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const actionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/actionLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
function ReviewAction({ disabled, onUpdate }) {
    return (<actionLink_1.default type="button" disabled={disabled} onAction={() => onUpdate({ inbox: false })} title={(0, locale_1.t)('Mark Reviewed')} icon={<icons_1.IconIssues size="xs"/>}>
      {(0, locale_1.t)('Mark Reviewed')}
    </actionLink_1.default>);
}
exports.default = ReviewAction;
//# sourceMappingURL=reviewAction.jsx.map