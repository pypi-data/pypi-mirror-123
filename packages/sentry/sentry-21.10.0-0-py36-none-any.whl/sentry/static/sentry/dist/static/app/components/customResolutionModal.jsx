Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_select_1 = require("react-select");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const forms_1 = require("app/components/forms");
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function VersionOption(_a) {
    var { data } = _a, props = (0, tslib_1.__rest)(_a, ["data"]);
    const release = data.release;
    return (<react_select_1.components.Option data={data} {...props}>
      <strong>
        <version_1.default version={release.version} anchor={false}/>
      </strong>
      <br />
      <small>
        {(0, locale_1.t)('Created')} <timeSince_1.default date={release.dateCreated}/>
      </small>
    </react_select_1.components.Option>);
}
class CustomResolutionModal extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            version: '',
        };
        this.onChange = (value) => {
            this.setState({ version: value }); // TODO(ts): Add select value type as generic to select controls
        };
        this.onAsyncFieldResults = (results) => results.map(release => ({
            value: release.version,
            label: release.version,
            release,
        }));
    }
    render() {
        const { orgSlug, projectSlug, closeModal, onSelected, Header, Body, Footer } = this.props;
        const url = projectSlug
            ? `/projects/${orgSlug}/${projectSlug}/releases/`
            : `/organizations/${orgSlug}/releases/`;
        const onSubmit = (e) => {
            e.preventDefault();
            onSelected({ inRelease: this.state.version });
            closeModal();
        };
        return (<form onSubmit={onSubmit}>
        <Header>{(0, locale_1.t)('Resolved In')}</Header>
        <Body>
          <forms_1.SelectAsyncField label={(0, locale_1.t)('Version')} id="version" name="version" onChange={this.onChange} placeholder={(0, locale_1.t)('e.g. 1.0.4')} url={url} onResults={this.onAsyncFieldResults} onQuery={query => ({ query })} components={{
                Option: VersionOption,
            }}/>
        </Body>
        <Footer>
          <button_1.default type="button" css={{ marginRight: (0, space_1.default)(1.5) }} onClick={closeModal}>
            {(0, locale_1.t)('Cancel')}
          </button_1.default>
          <button_1.default type="submit" priority="primary">
            {(0, locale_1.t)('Save Changes')}
          </button_1.default>
        </Footer>
      </form>);
    }
}
exports.default = CustomResolutionModal;
//# sourceMappingURL=customResolutionModal.jsx.map