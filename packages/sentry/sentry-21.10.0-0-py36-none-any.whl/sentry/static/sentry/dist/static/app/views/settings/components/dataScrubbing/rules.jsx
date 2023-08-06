Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("./types");
const utils_1 = require("./utils");
const getListItemDescription = (rule) => {
    const { method, type, source } = rule;
    const methodLabel = (0, utils_1.getMethodLabel)(method);
    const typeLabel = (0, utils_1.getRuleLabel)(type);
    const descriptionDetails = [];
    descriptionDetails.push(`[${methodLabel.label}]`);
    descriptionDetails.push(rule.type === types_1.RuleType.PATTERN ? `[${rule.pattern}]` : `[${typeLabel}]`);
    if (rule.method === types_1.MethodType.REPLACE && rule.placeholder) {
        descriptionDetails.push(` with [${rule.placeholder}]`);
    }
    return `${descriptionDetails.join(' ')} ${(0, locale_1.t)('from')} [${source}]`;
};
const Rules = React.forwardRef(function RulesList({ rules, onEditRule, onDeleteRule, disabled }, ref) {
    return (<List ref={ref} isDisabled={disabled} data-test-id="advanced-data-scrubbing-rules">
      {rules.map(rule => {
            const { id } = rule;
            return (<ListItem key={id}>
            <textOverflow_1.default>{getListItemDescription(rule)}</textOverflow_1.default>
            {onEditRule && (<button_1.default label={(0, locale_1.t)('Edit Rule')} size="small" onClick={onEditRule(id)} icon={<icons_1.IconEdit />} disabled={disabled}/>)}
            {onDeleteRule && (<button_1.default label={(0, locale_1.t)('Delete Rule')} size="small" onClick={onDeleteRule(id)} icon={<icons_1.IconDelete />} disabled={disabled}/>)}
          </ListItem>);
        })}
    </List>);
});
exports.default = Rules;
const List = (0, styled_1.default)('ul') `
  list-style: none;
  margin: 0;
  padding: 0;
  margin-bottom: 0 !important;
  ${p => p.isDisabled &&
    `
      color: ${p.theme.gray200};
      background: ${p.theme.backgroundSecondary};
  `}
`;
const ListItem = (0, styled_1.default)('li') `
  display: grid;
  grid-template-columns: auto max-content max-content;
  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.border};
  &:hover {
    background-color: ${p => p.theme.backgroundSecondary};
  }
  &:last-child {
    border-bottom: 0;
  }
`;
//# sourceMappingURL=rules.jsx.map