Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const settingsHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsHeader"));
/**
 * If `blendCorner` is false, then we apply border-radius to all corners
 *
 * Otherwise apply radius to opposite side of `alignMenu` *unles it is fixed width*
 */
const getMenuBorderRadius = ({ blendWithActor, blendCorner, alignMenu, width, theme, }) => {
    const radius = theme.borderRadius;
    if (!blendCorner) {
        return (0, react_1.css) `
      border-radius: ${radius};
    `;
    }
    // If menu width is the same width as the control
    const isFullWidth = width === '100%';
    // No top border radius if widths match
    const hasTopLeftRadius = !blendWithActor && !isFullWidth && alignMenu !== 'left';
    const hasTopRightRadius = !blendWithActor && !isFullWidth && !hasTopLeftRadius;
    return (0, react_1.css) `
    border-radius: ${hasTopLeftRadius ? radius : 0} ${hasTopRightRadius ? radius : 0}
      ${radius} ${radius};
  `;
};
const getMenuArrow = ({ menuWithArrow, alignMenu, theme }) => {
    if (!menuWithArrow) {
        return '';
    }
    const alignRight = alignMenu === 'right';
    return (0, react_1.css) `
    top: 32px;

    &::before {
      width: 0;
      height: 0;
      border-left: 9px solid transparent;
      border-right: 9px solid transparent;
      border-bottom: 9px solid rgba(52, 60, 69, 0.35);
      content: '';
      display: block;
      position: absolute;
      top: -9px;
      left: 10px;
      z-index: -2;
      ${alignRight && 'left: auto;'};
      ${alignRight && 'right: 10px;'};
    }

    &:after {
      width: 0;
      height: 0;
      border-left: 8px solid transparent;
      border-right: 8px solid transparent;
      border-bottom: 8px solid ${theme.background};
      content: '';
      display: block;
      position: absolute;
      top: -8px;
      left: 11px;
      z-index: -1;
      ${alignRight && 'left: auto;'};
      ${alignRight && 'right: 11px;'};
    }
  `;
};
const DropdownBubble = (0, styled_1.default)('div') `
  background: ${p => p.theme.background};
  color: ${p => p.theme.textColor};
  border: 1px solid ${p => p.theme.border};
  position: absolute;
  top: calc(100% - 1px);
  ${p => (p.width ? `width: ${p.width}` : '')};
  right: 0;
  box-shadow: ${p => p.theme.dropShadowLight};
  overflow: hidden;

  ${getMenuBorderRadius};
  ${({ alignMenu }) => (alignMenu === 'left' ? 'left: 0;' : '')};

  ${getMenuArrow};

  /* This is needed to be able to cover e.g. pagination buttons, but also be
   * below dropdown actor button's zindex */
  z-index: ${p => p.theme.zIndex.dropdownAutocomplete.menu};

  ${ /* sc-selector */settingsHeader_1.default} & {
    z-index: ${p => p.theme.zIndex.dropdownAutocomplete.menu + 2};
  }
`;
exports.default = DropdownBubble;
//# sourceMappingURL=dropdownBubble.jsx.map