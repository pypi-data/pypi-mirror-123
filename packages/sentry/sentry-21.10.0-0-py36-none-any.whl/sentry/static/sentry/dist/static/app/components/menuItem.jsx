Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const MenuItem = (_a) => {
    var { header, icon, divider, isActive, noAnchor, className, children } = _a, props = (0, tslib_1.__rest)(_a, ["header", "icon", "divider", "isActive", "noAnchor", "className", "children"]);
    const { to, href, title, withBorder, disabled, onSelect, eventKey, allowDefaultEvent, stopPropagation, } = props;
    const handleClick = (e) => {
        if (disabled) {
            return;
        }
        if (onSelect) {
            if (allowDefaultEvent !== true) {
                e.preventDefault();
            }
            if (stopPropagation) {
                e.stopPropagation();
            }
            (0, callIfFunction_1.callIfFunction)(onSelect, eventKey);
        }
    };
    const renderAnchor = () => {
        const linkProps = {
            onClick: handleClick,
            tabIndex: -1,
            isActive,
            disabled,
            withBorder,
        };
        if (to) {
            return (<MenuLink to={to} {...linkProps} title={title}>
          {icon && <MenuIcon>{icon}</MenuIcon>}
          {children}
        </MenuLink>);
        }
        if (href) {
            return (<MenuAnchor {...linkProps} href={href}>
          {icon && <MenuIcon>{icon}</MenuIcon>}
          {children}
        </MenuAnchor>);
        }
        return (<MenuTarget role="button" {...linkProps} title={title}>
        {icon && <MenuIcon>{icon}</MenuIcon>}
        {children}
      </MenuTarget>);
    };
    let renderChildren = null;
    if (noAnchor) {
        renderChildren = children;
    }
    else if (header) {
        renderChildren = children;
    }
    else if (!divider) {
        renderChildren = renderAnchor();
    }
    return (<MenuListItem className={className} role="presentation" isActive={isActive} divider={divider} noAnchor={noAnchor} header={header} {...(0, omit_1.default)(props, ['href', 'title', 'onSelect', 'eventKey', 'to', 'as'])}>
      {renderChildren}
    </MenuListItem>);
};
function getListItemStyles(props) {
    const common = `
    display: block;
    padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(2)};
    &:focus {
      outline: none;
    }
  `;
    if (props.disabled) {
        return `
      ${common}
      color: ${props.theme.disabled};
      background: transparent;
      cursor: not-allowed;
    `;
    }
    if (props.isActive) {
        return `
      ${common}
      color: ${props.theme.white};
      background: ${props.theme.active};

      &:hover {
        color: ${props.theme.black};
      }
    `;
    }
    return `
    ${common}

    &:hover {
      background: ${props.theme.focus};
    }
  `;
}
function getChildStyles(props) {
    if (!props.noAnchor) {
        return '';
    }
    return `
    & a {
      ${getListItemStyles(props)}
    }
  `;
}
const shouldForwardProp = (p) => typeof p === 'string' && ['isActive', 'disabled', 'withBorder'].includes(p) === false;
const MenuAnchor = (0, styled_1.default)('a', { shouldForwardProp }) `
  ${getListItemStyles}
`;
const MenuListItem = (0, styled_1.default)('li') `
  display: block;

  ${p => p.withBorder &&
    `
    border-bottom: 1px solid ${p.theme.innerBorder};

    &:last-child {
      border-bottom: none;
    }
  `};
  ${p => p.divider &&
    `
    height: 1px;
    margin: ${(0, space_1.default)(0.5)} 0;
    overflow: hidden;
    background-color: ${p.theme.innerBorder};
  `}
  ${p => p.header &&
    `
    padding: ${(0, space_1.default)(0.25)} ${(0, space_1.default)(0.5)};
    font-size: ${p.theme.fontSizeSmall};
    line-height: 1.4;
    color: ${p.theme.gray300};
  `}

  ${getChildStyles}
`;
const MenuTarget = (0, styled_1.default)('span') `
  ${getListItemStyles}
  display: flex;
  align-items: center;
`;
const MenuIcon = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin-right: ${(0, space_1.default)(1)};
`;
const MenuLink = (0, styled_1.default)(link_1.default, { shouldForwardProp }) `
  ${getListItemStyles}
`;
exports.default = MenuItem;
//# sourceMappingURL=menuItem.jsx.map