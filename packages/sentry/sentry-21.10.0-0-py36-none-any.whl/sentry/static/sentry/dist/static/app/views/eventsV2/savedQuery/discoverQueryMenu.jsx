Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const DiscoverQueryMenu = ({ children }) => (<dropdownMenu_1.default>
    {({ isOpen, getRootProps, getActorProps, getMenuProps }) => {
        const topLevelCx = (0, classnames_1.default)('dropdown', {
            'anchor-right': true,
            open: isOpen,
        });
        return (<span {...getRootProps({
            className: topLevelCx,
        })}>
          <DropdownTarget {...getActorProps({
            onClick: (event) => {
                event.stopPropagation();
                event.preventDefault();
            },
        })}>
            <button_1.default size="small">
              <icons_1.IconEllipsis data-test-id="context-menu" size="md"/>
            </button_1.default>
          </DropdownTarget>
          {isOpen && (<Menu {...getMenuProps({})} className={(0, classnames_1.default)('dropdown-menu')}>
              {children}
            </Menu>)}
        </span>);
    }}
  </dropdownMenu_1.default>);
const DropdownTarget = (0, styled_1.default)('div') `
  display: flex;
  cursor: pointer;
`;
const Menu = (0, styled_1.default)('ul') `
  margin-top: ${(0, space_1.default)(2)};
  margin-right: ${(0, space_1.default)(0.25)};
`;
exports.default = DiscoverQueryMenu;
//# sourceMappingURL=discoverQueryMenu.jsx.map