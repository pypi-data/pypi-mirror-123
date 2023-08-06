Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const menu_1 = (0, tslib_1.__importDefault)(require("./menu"));
const DropdownAutoComplete = (_a) => {
    var { allowActorToggle = false, children } = _a, props = (0, tslib_1.__rest)(_a, ["allowActorToggle", "children"]);
    return (<menu_1.default {...props}>
    {renderProps => {
            const { isOpen, actions, getActorProps } = renderProps;
            // Don't pass `onClick` from `getActorProps`
            const _a = getActorProps(), { onClick: _onClick } = _a, actorProps = (0, tslib_1.__rest)(_a, ["onClick"]);
            return (<Actor isOpen={isOpen} role="button" tabIndex={0} onClick={isOpen && allowActorToggle ? actions.close : actions.open} {...actorProps}>
          {children(renderProps)}
        </Actor>);
        }}
  </menu_1.default>);
};
const Actor = (0, styled_1.default)('div') `
  position: relative;
  width: 100%;
  /* This is needed to be able to cover dropdown menu so that it looks like one unit */
  ${p => p.isOpen && `z-index: ${p.theme.zIndex.dropdownAutocomplete.actor}`};
`;
exports.default = DropdownAutoComplete;
//# sourceMappingURL=index.jsx.map