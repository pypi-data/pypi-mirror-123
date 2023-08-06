Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const icons_1 = require("app/icons");
const getRootCss = (theme) => (0, react_1.css) `
  .dropdown-menu {
    & > li > a {
      color: ${theme.textColor};

      &:hover,
      &:focus {
        color: inherit;
        background-color: ${theme.focus};
      }
    }

    & .disabled {
      cursor: not-allowed;
      &:hover {
        background: inherit;
        color: inherit;
      }
    }
  }

  .dropdown-submenu:hover > span {
    color: ${theme.textColor};
    background: ${theme.focus};
  }
`;
function DropdownLink(_a) {
    var { anchorMiddle, title, customTitle, children, menuClasses, className, topLevelClasses, anchorRight = false, disabled = false, caret = true, alwaysRenderMenu = true } = _a, otherProps = (0, tslib_1.__rest)(_a, ["anchorMiddle", "title", "customTitle", "children", "menuClasses", "className", "topLevelClasses", "anchorRight", "disabled", "caret", "alwaysRenderMenu"]);
    const theme = (0, react_1.useTheme)();
    return (<dropdownMenu_1.default alwaysRenderMenu={alwaysRenderMenu} {...otherProps}>
      {({ isOpen, getRootProps, getActorProps, getMenuProps }) => {
            const shouldRenderMenu = alwaysRenderMenu || isOpen;
            const cx = (0, classnames_1.default)('dropdown-actor', className, {
                'dropdown-menu-right': anchorRight,
                'dropdown-toggle': true,
                hover: isOpen,
                disabled,
            });
            const topLevelCx = (0, classnames_1.default)('dropdown', topLevelClasses, {
                'pull-right': anchorRight,
                'anchor-right': anchorRight,
                'anchor-middle': anchorMiddle,
                open: isOpen,
            });
            return (<span css={getRootCss(theme)} {...getRootProps({
                className: topLevelCx,
            })}>
            <a {...getActorProps({
                className: cx,
            })}>
              {customTitle || (<div className="dropdown-actor-title">
                  {title}
                  {caret && <icons_1.IconChevron direction={isOpen ? 'up' : 'down'} size="xs"/>}
                </div>)}
            </a>

            {shouldRenderMenu && (<ul {...getMenuProps({
                    className: (0, classnames_1.default)(menuClasses, 'dropdown-menu'),
                })}>
                {children}
              </ul>)}
          </span>);
        }}
    </dropdownMenu_1.default>);
}
exports.default = DropdownLink;
//# sourceMappingURL=dropdownLink.jsx.map