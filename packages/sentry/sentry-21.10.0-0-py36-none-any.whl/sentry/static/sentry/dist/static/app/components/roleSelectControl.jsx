Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_select_1 = require("react-select");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
function RoleSelectControl(_a) {
    var { roles, disableUnallowed } = _a, props = (0, tslib_1.__rest)(_a, ["roles", "disableUnallowed"]);
    return (<selectControl_1.default options={roles === null || roles === void 0 ? void 0 : roles.map((r) => ({
            value: r.id,
            label: r.name,
            disabled: disableUnallowed && !r.allowed,
            description: r.desc,
        }))} components={{
            Option: (_a) => {
                var { label, data } = _a, optionProps = (0, tslib_1.__rest)(_a, ["label", "data"]);
                return (<react_select_1.components.Option label={label} {...optionProps}>
            <RoleItem>
              <h1>{label}</h1>
              <div>{data.description}</div>
            </RoleItem>
          </react_select_1.components.Option>);
            },
        }} styles={{
            control: provided => (Object.assign(Object.assign({}, provided), { borderBottomLeftRadius: theme_1.default.borderRadius, borderBottomRightRadius: theme_1.default.borderRadius })),
            menu: provided => (Object.assign(Object.assign({}, provided), { borderRadius: theme_1.default.borderRadius, marginTop: (0, space_1.default)(0.5), width: '350px', overflow: 'hidden' })),
        }} {...props}/>);
}
const RoleItem = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 80px 1fr;
  grid-gap: ${(0, space_1.default)(1)};

  h1,
  div {
    font-size: ${p => p.theme.fontSizeSmall};
    line-height: 1.4;
    margin: ${(0, space_1.default)(0.25)} 0;
  }
`;
exports.default = RoleSelectControl;
//# sourceMappingURL=roleSelectControl.jsx.map