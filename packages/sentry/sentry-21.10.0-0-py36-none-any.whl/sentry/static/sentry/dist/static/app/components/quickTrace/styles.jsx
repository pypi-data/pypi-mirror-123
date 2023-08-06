Object.defineProperty(exports, "__esModule", { value: true });
exports.SingleEventHoverText = exports.ExternalDropdownLink = exports.ErrorNodeContent = exports.QuickTraceValue = exports.DropdownItemSubContainer = exports.DropdownItem = exports.DropdownMenuHeader = exports.DropdownContainer = exports.TraceConnector = exports.EventNode = exports.QuickTraceContainer = exports.SectionSubtext = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const menuHeader_1 = (0, tslib_1.__importDefault)(require("app/components/actions/menuHeader"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const tag_1 = (0, tslib_1.__importStar)(require("app/components/tag"));
const truncate_1 = (0, tslib_1.__importDefault)(require("app/components/truncate"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const formatters_1 = require("app/utils/formatters");
exports.SectionSubtext = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
`;
exports.QuickTraceContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  height: 24px;
`;
const nodeColors = (theme) => ({
    error: {
        color: theme.white,
        background: theme.red300,
        border: theme.red300,
    },
    warning: {
        color: theme.red300,
        background: theme.background,
        border: theme.red300,
    },
    white: {
        color: theme.textColor,
        background: theme.background,
        border: theme.textColor,
    },
    black: {
        color: theme.background,
        background: theme.textColor,
        border: theme.textColor,
    },
});
exports.EventNode = (0, styled_1.default)(tag_1.default) `
  span {
    display: flex;
    color: ${p => nodeColors(p.theme)[p.type || 'white'].color};
  }
  & ${ /* sc-selector */tag_1.Background} {
    background-color: ${p => nodeColors(p.theme)[p.type || 'white'].background};
    border: 1px solid ${p => nodeColors(p.theme)[p.type || 'white'].border};
  }

  /*
   * When the EventNode is contains an icon, we need to offset the
   * component a little for all the EventNodes to be aligned.
   */
  ${p => p.shouldOffset && `margin-top: ${(0, space_1.default)(0.5)}`}
`;
exports.TraceConnector = (0, styled_1.default)('div') `
  width: ${(0, space_1.default)(1)};
  border-top: 1px solid ${p => p.theme.textColor};
`;
/**
 * The DropdownLink component is styled directly with less and the way the
 * elements are laid out within means we can't apply any styles directly
 * using emotion. Instead, we wrap it all inside a span and indirectly
 * style it here.
 */
exports.DropdownContainer = (0, styled_1.default)('span') `
  .dropdown-menu {
    padding: 0;
  }
`;
exports.DropdownMenuHeader = (0, styled_1.default)(menuHeader_1.default) `
  background: ${p => p.theme.backgroundSecondary};
  ${p => p.first && 'border-radius: 2px'};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(1.5)};
`;
const StyledMenuItem = (0, styled_1.default)(menuItem_1.default) `
  width: ${p => (p.width === 'large' ? '350px' : '200px')};

  &:not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.innerBorder};
  }
`;
const MenuItemContent = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  width: 100%;
`;
function DropdownItem({ children, onSelect, allowDefaultEvent, to, width = 'large', }) {
    return (<StyledMenuItem to={to} onSelect={onSelect} width={width} allowDefaultEvent={allowDefaultEvent}>
      <MenuItemContent>{children}</MenuItemContent>
    </StyledMenuItem>);
}
exports.DropdownItem = DropdownItem;
exports.DropdownItemSubContainer = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;

  > a {
    padding-left: 0 !important;
  }
`;
exports.QuickTraceValue = (0, styled_1.default)(truncate_1.default) `
  padding-left: ${(0, space_1.default)(1)};
  white-space: nowrap;
`;
exports.ErrorNodeContent = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: repeat(2, auto);
  grid-gap: ${(0, space_1.default)(0.25)};
  align-items: center;
`;
exports.ExternalDropdownLink = (0, styled_1.default)(externalLink_1.default) `
  display: inherit !important;
  padding: 0 !important;
  color: ${p => p.theme.textColor};
  &:hover {
    color: ${p => p.theme.textColor};
  }
`;
function SingleEventHoverText({ event }) {
    return (<div>
      <truncate_1.default value={event.transaction} maxLength={30} leftTrim trimRegex={/\.|\//g} expandable={false}/>
      <div>
        {(0, formatters_1.getDuration)(event['transaction.duration'] / 1000, event['transaction.duration'] < 1000 ? 0 : 2, true)}
      </div>
    </div>);
}
exports.SingleEventHoverText = SingleEventHoverText;
//# sourceMappingURL=styles.jsx.map