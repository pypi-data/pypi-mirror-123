Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupingValue = exports.GroupingComponentListItem = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const groupingComponentChildren_1 = (0, tslib_1.__importDefault)(require("./groupingComponentChildren"));
const groupingComponentStacktrace_1 = (0, tslib_1.__importDefault)(require("./groupingComponentStacktrace"));
const utils_1 = require("./utils");
const GroupingComponent = ({ component, showNonContributing }) => {
    const shouldInlineValue = (0, utils_1.shouldInlineComponentValue)(component);
    const GroupingComponentListItems = component.id === 'stacktrace'
        ? groupingComponentStacktrace_1.default
        : groupingComponentChildren_1.default;
    return (<GroupingComponentWrapper isContributing={component.contributes}>
      <span>
        {component.name || component.id}
        {component.hint && <GroupingHint>{` (${component.hint})`}</GroupingHint>}
      </span>

      <GroupingComponentList isInline={shouldInlineValue}>
        <GroupingComponentListItems component={component} showNonContributing={showNonContributing}/>
      </GroupingComponentList>
    </GroupingComponentWrapper>);
};
const GroupingComponentList = (0, styled_1.default)('ul') `
  padding: 0;
  margin: 0;
  list-style: none;
  &,
  & > li {
    display: ${p => (p.isInline ? 'inline' : 'block')};
  }
`;
exports.GroupingComponentListItem = (0, styled_1.default)('li') `
  padding: 0;
  margin: ${(0, space_1.default)(0.25)} 0 ${(0, space_1.default)(0.25)} ${(0, space_1.default)(1.5)};

  ${p => p.isCollapsible &&
    `
    border-left: 1px solid ${p.theme.innerBorder};
    margin: 0 0 -${(0, space_1.default)(0.25)} ${(0, space_1.default)(1)};
    padding-left: ${(0, space_1.default)(0.5)};
  `}
`;
exports.GroupingValue = (0, styled_1.default)('code') `
  display: inline-block;
  margin: ${(0, space_1.default)(0.25)} ${(0, space_1.default)(0.5)} ${(0, space_1.default)(0.25)} 0;
  font-size: ${p => p.theme.fontSizeSmall};
  padding: 0 ${(0, space_1.default)(0.25)};
  background: rgba(112, 163, 214, 0.1);
  color: ${p => p.theme.textColor};

  ${({ valueType }) => (valueType === 'function' || valueType === 'symbol') &&
    `
    font-weight: bold;
    color: ${p => p.theme.textColor};
  `}
`;
const GroupingComponentWrapper = (0, styled_1.default)('div') `
  color: ${p => (p.isContributing ? null : p.theme.textColor)};

  ${exports.GroupingValue}, button {
    opacity: 1;
  }
`;
const GroupingHint = (0, styled_1.default)('small') `
  font-size: 0.8em;
`;
exports.default = GroupingComponent;
//# sourceMappingURL=groupingComponent.jsx.map