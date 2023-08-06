Object.defineProperty(exports, "__esModule", { value: true });
exports.Background = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const TAG_HEIGHT = '20px';
function Tag(_a) {
    var { type = 'default', icon, tooltipText, to, onClick, href, onDismiss, children, textMaxWidth = 150 } = _a, props = (0, tslib_1.__rest)(_a, ["type", "icon", "tooltipText", "to", "onClick", "href", "onDismiss", "children", "textMaxWidth"]);
    const iconsProps = {
        size: '11px',
        color: theme_1.default.tag[type].iconColor,
    };
    const tag = (<tooltip_1.default title={tooltipText} containerDisplayMode="inline-flex">
      <exports.Background type={type}>
        {tagIcon()}

        <Text type={type} maxWidth={textMaxWidth}>
          {children}
        </Text>

        {(0, utils_1.defined)(onDismiss) && (<DismissButton onClick={handleDismiss} size="zero" priority="link" label={(0, locale_1.t)('Dismiss')}>
            <icons_1.IconClose isCircled {...iconsProps}/>
          </DismissButton>)}
      </exports.Background>
    </tooltip_1.default>);
    function handleDismiss(event) {
        event.preventDefault();
        onDismiss === null || onDismiss === void 0 ? void 0 : onDismiss();
    }
    function tagIcon() {
        if (React.isValidElement(icon)) {
            return <IconWrapper>{React.cloneElement(icon, Object.assign({}, iconsProps))}</IconWrapper>;
        }
        if (((0, utils_1.defined)(href) || (0, utils_1.defined)(to)) && icon === undefined) {
            return (<IconWrapper>
          <icons_1.IconOpen {...iconsProps}/>
        </IconWrapper>);
        }
        return null;
    }
    function tagWithParent() {
        if ((0, utils_1.defined)(href)) {
            return <externalLink_1.default href={href}>{tag}</externalLink_1.default>;
        }
        if ((0, utils_1.defined)(to) && (0, utils_1.defined)(onClick)) {
            return (<link_1.default to={to} onClick={onClick}>
          {tag}
        </link_1.default>);
        }
        else if ((0, utils_1.defined)(to)) {
            return <link_1.default to={to}>{tag}</link_1.default>;
        }
        return tag;
    }
    return <TagWrapper {...props}>{tagWithParent()}</TagWrapper>;
}
const TagWrapper = (0, styled_1.default)('span') `
  font-size: ${p => p.theme.fontSizeSmall};
`;
exports.Background = (0, styled_1.default)('div') `
  display: inline-flex;
  align-items: center;
  height: ${TAG_HEIGHT};
  border-radius: ${TAG_HEIGHT};
  background-color: ${p => p.theme.tag[p.type].background};
  padding: 0 ${(0, space_1.default)(1)};
`;
const IconWrapper = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(0.5)};
  display: inline-flex;
`;
const Text = (0, styled_1.default)('span') `
  color: ${p => (['black', 'focus'].includes(p.type) ? p.theme.white : p.theme.gray500)};
  max-width: ${p => p.maxWidth}px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  line-height: ${TAG_HEIGHT};
`;
const DismissButton = (0, styled_1.default)(button_1.default) `
  margin-left: ${(0, space_1.default)(0.5)};
  border: none;
`;
exports.default = Tag;
//# sourceMappingURL=tag.jsx.map