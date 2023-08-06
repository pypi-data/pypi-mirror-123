Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/actions/button"));
const button_2 = (0, tslib_1.__importDefault)(require("app/components/button"));
const debugFileSources_1 = require("app/data/debugFileSources");
const iconClose_1 = require("app/icons/iconClose");
const locale_1 = require("app/locale");
const input_1 = require("app/styles/input");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const guid_1 = require("app/utils/guid");
const input_2 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
const CLEAR_PASSWORD_BUTTON_SIZE = 22;
const PASSWORD_INPUT_PADDING_RIGHT = input_1.INPUT_PADDING + CLEAR_PASSWORD_BUTTON_SIZE;
function Http(_a) {
    var _b, _c, _d, _e, _f, _g, _h, _j;
    var { Header, Body, Footer, onSubmit } = _a, props = (0, tslib_1.__rest)(_a, ["Header", "Body", "Footer", "onSubmit"]);
    const initialData = {
        name: (_b = props.initialData) === null || _b === void 0 ? void 0 : _b.name,
        url: (_c = props.initialData) === null || _c === void 0 ? void 0 : _c.url,
        username: (_d = props.initialData) === null || _d === void 0 ? void 0 : _d.username,
        password: typeof ((_e = props.initialData) === null || _e === void 0 ? void 0 : _e.password) === 'object' ? undefined : '',
        'layout.type': (_g = (_f = props.initialData) === null || _f === void 0 ? void 0 : _f.layout.type) !== null && _g !== void 0 ? _g : 'native',
        'layout.casing': (_j = (_h = props.initialData) === null || _h === void 0 ? void 0 : _h.layout.casing) !== null && _j !== void 0 ? _j : 'default',
    };
    const [data, setData] = (0, react_1.useState)(initialData);
    function isFormInvalid() {
        return !data.name || !data.url;
    }
    function formUnchanged() {
        return data === initialData;
    }
    function handleSubmit() {
        const validData = data;
        onSubmit({
            id: (0, guid_1.uniqueId)(),
            name: validData.name,
            url: validData.url,
            'layout.type': validData['layout.type'],
            'layout.casing': validData['layout.casing'],
            username: validData.username,
            password: validData.password === undefined
                ? { 'hidden-secret': true }
                : !validData.password
                    ? undefined
                    : validData.password,
        });
    }
    function handleClearPassword() {
        setData(Object.assign(Object.assign({}, data), { password: '' }));
    }
    return (<react_1.Fragment>
      <Header closeButton>
        {initialData
            ? (0, locale_1.tct)('Update [name] Repository', { name: debugFileSources_1.DEBUG_SOURCE_TYPES.http })
            : (0, locale_1.tct)('Add [name] Repository', { name: debugFileSources_1.DEBUG_SOURCE_TYPES.http })}
      </Header>
      <Body>
        <field_1.default label={(0, locale_1.t)('Name')} inline={false} help={(0, locale_1.t)('A display name for this repository')} flexibleControlStateSize stacked required>
          <input_2.default type="text" name="name" placeholder={(0, locale_1.t)('New Repository')} value={data.name} onChange={e => setData(Object.assign(Object.assign({}, data), { name: e.target.value }))}/>
        </field_1.default>
        <hr />
        <field_1.default label={(0, locale_1.t)('Download Url')} inline={false} help={(0, locale_1.t)('Full URL to the symbol server')} flexibleControlStateSize stacked required>
          <input_2.default type="text" name="url" placeholder="https://msdl.microsoft.com/download/symbols/" value={data.url} onChange={e => setData(Object.assign(Object.assign({}, data), { url: e.target.value }))}/>
        </field_1.default>
        <field_1.default label={(0, locale_1.t)('User')} inline={false} help={(0, locale_1.t)('User for HTTP basic auth')} flexibleControlStateSize stacked>
          <input_2.default type="text" name="username" placeholder="admin" value={data.username} onChange={e => setData(Object.assign(Object.assign({}, data), { username: e.target.value }))}/>
        </field_1.default>
        <field_1.default label={(0, locale_1.t)('Password')} inline={false} help={(0, locale_1.t)('Password for HTTP basic auth')} flexibleControlStateSize stacked>
          <PasswordInput type={data.password === undefined ? 'text' : 'password'} name="url" placeholder={data.password === undefined ? (0, locale_1.t)('(Password unchanged)') : 'open-sesame'} value={data.password} onChange={e => setData(Object.assign(Object.assign({}, data), { password: e.target.value }))}/>
          {(data.password === undefined ||
            (typeof data.password === 'string' && !!data.password)) && (<ClearPasswordButton onClick={handleClearPassword} icon={<iconClose_1.IconClose size="14px"/>} size="xsmall" title={(0, locale_1.t)('Clear password')} label={(0, locale_1.t)('Clear password')} borderless/>)}
        </field_1.default>
        <hr />
        <StyledSelectField name="layout.type" label={(0, locale_1.t)('Directory Layout')} help={(0, locale_1.t)('The layout of the folder structure.')} options={Object.keys(debugFileSources_1.DEBUG_SOURCE_LAYOUTS).map(key => ({
            value: key,
            label: debugFileSources_1.DEBUG_SOURCE_LAYOUTS[key],
        }))} value={data['layout.type']} onChange={value => setData(Object.assign(Object.assign({}, data), { ['layout.type']: value }))} inline={false} flexibleControlStateSize stacked/>
        <StyledSelectField name="layout.casing" label={(0, locale_1.t)('Path Casing')} help={(0, locale_1.t)('The case of files and folders.')} options={Object.keys(debugFileSources_1.DEBUG_SOURCE_CASINGS).map(key => ({
            value: key,
            label: debugFileSources_1.DEBUG_SOURCE_CASINGS[key],
        }))} value={data['layout.casing']} onChange={value => setData(Object.assign(Object.assign({}, data), { ['layout.casing']: value }))} inline={false} flexibleControlStateSize stacked/>
      </Body>
      <Footer>
        <button_2.default onClick={handleSubmit} priority="primary" disabled={isFormInvalid() || formUnchanged()}>
          {(0, locale_1.t)('Save changes')}
        </button_2.default>
      </Footer>
    </react_1.Fragment>);
}
exports.default = Http;
const StyledSelectField = (0, styled_1.default)(selectField_1.default) `
  padding-right: 0;
`;
const PasswordInput = (0, styled_1.default)(input_2.default) `
  padding-right: ${PASSWORD_INPUT_PADDING_RIGHT}px;
`;
const ClearPasswordButton = (0, styled_1.default)(button_1.default) `
  background: transparent;
  height: ${CLEAR_PASSWORD_BUTTON_SIZE}px;
  width: ${CLEAR_PASSWORD_BUTTON_SIZE}px;
  padding: 0;
  position: absolute;
  top: 50%;
  right: ${(0, space_1.default)(0.75)};
  transform: translateY(-50%);
  svg {
    color: ${p => p.theme.gray400};
    :hover {
      color: hsl(0, 0%, 60%);
    }
  }
`;
//# sourceMappingURL=http.jsx.map