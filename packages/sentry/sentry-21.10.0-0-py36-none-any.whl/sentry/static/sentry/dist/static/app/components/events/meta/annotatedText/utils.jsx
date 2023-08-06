Object.defineProperty(exports, "__esModule", { value: true });
exports.getTooltipText = void 0;
const locale_1 = require("app/locale");
const REMARKS = {
    a: 'Annotated',
    x: 'Removed',
    s: 'Replaced',
    m: 'Masked',
    p: 'Pseudonymized',
    e: 'Encrypted',
};
const KNOWN_RULES = {
    '!limit': 'size limits',
    '!raw': 'raw payload',
    '!config': 'SDK configuration',
};
function getTooltipText({ remark = '', rule_id: rule = '', }) {
    const remark_title = REMARKS[remark];
    const rule_title = KNOWN_RULES[rule] || (0, locale_1.t)('PII rule "%s"', rule);
    if (remark_title) {
        return (0, locale_1.t)('%s because of %s', remark_title, rule_title);
    }
    return rule_title;
}
exports.getTooltipText = getTooltipText;
//# sourceMappingURL=utils.jsx.map