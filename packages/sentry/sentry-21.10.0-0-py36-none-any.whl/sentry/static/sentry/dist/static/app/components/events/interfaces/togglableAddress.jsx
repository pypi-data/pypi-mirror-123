Object.defineProperty(exports, "__esModule", { value: true });
exports.AddressToggleIcon = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("app/components/events/interfaces/utils");
const stacktracePreview_1 = require("app/components/stacktracePreview");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const TogglableAddress = ({ startingAddress, address, relativeAddressMaxlength, isInlineFrame, isFoundByStackScanning, isAbsolute, onToggle, isHoverPreviewed, className, }) => {
    const convertAbsoluteAddressToRelative = () => {
        if (!startingAddress) {
            return '';
        }
        const relativeAddress = (0, utils_1.formatAddress)((0, utils_1.parseAddress)(address) - (0, utils_1.parseAddress)(startingAddress), relativeAddressMaxlength);
        return `+${relativeAddress}`;
    };
    const getAddressTooltip = () => {
        if (isInlineFrame && isFoundByStackScanning) {
            return (0, locale_1.t)('Inline frame, found by stack scanning');
        }
        if (isInlineFrame) {
            return (0, locale_1.t)('Inline frame');
        }
        if (isFoundByStackScanning) {
            return (0, locale_1.t)('Found by stack scanning');
        }
        return undefined;
    };
    const relativeAddress = convertAbsoluteAddressToRelative();
    const canBeConverted = !!(onToggle && relativeAddress);
    const formattedAddress = !relativeAddress || isAbsolute ? address : relativeAddress;
    const tooltipTitle = getAddressTooltip();
    const tooltipDelay = isHoverPreviewed ? stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY : undefined;
    return (<Wrapper className={className}>
      {canBeConverted && (<AddressIconTooltip title={isAbsolute ? (0, locale_1.t)('Switch to relative') : (0, locale_1.t)('Switch to absolute')} containerDisplayMode="inline-flex" delay={tooltipDelay}>
          <AddressToggleIcon onClick={onToggle} size="xs" color="purple300"/>
        </AddressIconTooltip>)}
      <tooltip_1.default title={tooltipTitle} disabled={!(isFoundByStackScanning || isInlineFrame)} delay={tooltipDelay}>
        <Address isFoundByStackScanning={isFoundByStackScanning} isInlineFrame={isInlineFrame} canBeConverted={canBeConverted}>
          {formattedAddress}
        </Address>
      </tooltip_1.default>
    </Wrapper>);
};
const AddressIconTooltip = (0, styled_1.default)(tooltip_1.default) `
  align-items: center;
  margin-right: ${(0, space_1.default)(0.75)};
`;
const AddressToggleIcon = (0, styled_1.default)(icons_1.IconFilter) `
  cursor: pointer;
  visibility: hidden;
  display: none;
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
  }
`;
exports.AddressToggleIcon = AddressToggleIcon;
const getAddresstextBorderBottom = (p) => {
    if (p.isFoundByStackScanning) {
        return `1px dashed ${p.theme.red300}`;
    }
    if (p.isInlineFrame) {
        return `1px dashed ${p.theme.blue300}`;
    }
    return 'none';
};
const Address = (0, styled_1.default)('span') `
  border-bottom: ${getAddresstextBorderBottom};
  white-space: nowrap;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    padding-left: ${p => (p.canBeConverted ? null : '18px')};
  }
`;
const Wrapper = (0, styled_1.default)('span') `
  font-family: ${p => p.theme.text.familyMono};
  font-size: ${p => p.theme.fontSizeExtraSmall};
  color: ${p => p.theme.textColor};
  letter-spacing: -0.25px;
  width: 100%;
  flex-grow: 0;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  padding: 0 ${(0, space_1.default)(0.5)} 0 0;
  order: 1;

  @media (min-width: ${props => props.theme.breakpoints[0]}) {
    padding: 0 ${(0, space_1.default)(0.5)};
    order: 0;
  }
`;
exports.default = TogglableAddress;
//# sourceMappingURL=togglableAddress.jsx.map