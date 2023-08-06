Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const richHttpContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/richHttpContent/richHttpContent"));
const utils_1 = require("app/components/events/interfaces/utils");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const truncate_1 = (0, tslib_1.__importDefault)(require("app/components/truncate"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/utils");
class RequestInterface extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            view: 'formatted',
        };
        this.isPartial = () => 
        // We assume we only have a partial interface is we're missing
        // an HTTP method. This means we don't have enough information
        // to reliably construct a full HTTP request.
        !this.props.data.method || !this.props.data.url;
        this.toggleView = (value) => {
            this.setState({
                view: value,
            });
        };
    }
    render() {
        const { data, type } = this.props;
        const view = this.state.view;
        let fullUrl = (0, utils_1.getFullUrl)(data);
        if (!(0, utils_2.isUrl)(fullUrl)) {
            // Check if the url passed in is a safe url to avoid XSS
            fullUrl = undefined;
        }
        let parsedUrl = null;
        if (fullUrl) {
            // use html tag to parse url, lol
            parsedUrl = document.createElement('a');
            parsedUrl.href = fullUrl;
        }
        let actions = null;
        if (!this.isPartial() && fullUrl) {
            actions = (<buttonBar_1.default merged active={view}>
          <button_1.default barId="formatted" size="xsmall" onClick={this.toggleView.bind(this, 'formatted')}>
            {/* Translators: this means "formatted" rendering (fancy tables) */}
            {(0, locale_1.t)('Formatted')}
          </button_1.default>
          <MonoButton barId="curl" size="xsmall" onClick={this.toggleView.bind(this, 'curl')}>
            curl
          </MonoButton>
        </buttonBar_1.default>);
        }
        const title = (<Header key="title">
        <externalLink_1.default href={fullUrl} title={fullUrl}>
          <Path>
            <strong>{data.method || 'GET'}</strong>
            <truncate_1.default value={parsedUrl ? parsedUrl.pathname : ''} maxLength={36} leftTrim/>
          </Path>
          {fullUrl && <StyledIconOpen size="xs"/>}
        </externalLink_1.default>
        <small>{parsedUrl ? parsedUrl.hostname : ''}</small>
      </Header>);
        return (<eventDataSection_1.default type={type} title={title} actions={actions} wrapTitle={false} className="request">
        {view === 'curl' ? (<pre>{(0, utils_1.getCurlCommand)(data)}</pre>) : (<richHttpContent_1.default data={data}/>)}
      </eventDataSection_1.default>);
    }
}
const MonoButton = (0, styled_1.default)(button_1.default) `
  font-family: ${p => p.theme.text.familyMono};
`;
const Path = (0, styled_1.default)('span') `
  color: ${p => p.theme.textColor};
  text-transform: none;
  font-weight: normal;

  & strong {
    margin-right: ${(0, space_1.default)(0.5)};
  }
`;
const Header = (0, styled_1.default)('h3') `
  display: flex;
  align-items: center;
`;
// Nudge the icon down so it is centered. the `external-icon` class
// doesn't quite get it in place.
const StyledIconOpen = (0, styled_1.default)(icons_1.IconOpen) `
  transition: 0.1s linear color;
  margin: 0 ${(0, space_1.default)(0.5)};
  color: ${p => p.theme.gray200};
  position: relative;
  top: 1px;

  &:hover {
    color: ${p => p.theme.subText};
  }
`;
exports.default = RequestInterface;
//# sourceMappingURL=request.jsx.map