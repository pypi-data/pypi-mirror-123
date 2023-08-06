Object.defineProperty(exports, "__esModule", { value: true });
exports.DownloadStatus = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dataExport_1 = require("app/components/dataExport");
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const layout_1 = (0, tslib_1.__importDefault)(require("app/views/auth/layout"));
var DownloadStatus;
(function (DownloadStatus) {
    DownloadStatus["Early"] = "EARLY";
    DownloadStatus["Valid"] = "VALID";
    DownloadStatus["Expired"] = "EXPIRED";
})(DownloadStatus = exports.DownloadStatus || (exports.DownloadStatus = {}));
class DataDownload extends asyncView_1.default {
    getTitle() {
        return (0, locale_1.t)('Download Center');
    }
    getEndpoints() {
        const { orgId, dataExportId } = this.props.params;
        return [['download', `/organizations/${orgId}/data-export/${dataExportId}/`]];
    }
    getActionLink(queryType) {
        const { orgId } = this.props.params;
        switch (queryType) {
            case dataExport_1.ExportQueryType.IssuesByTag:
                return `/organizations/${orgId}/issues/`;
            case dataExport_1.ExportQueryType.Discover:
                return `/organizations/${orgId}/discover/queries/`;
            default:
                return '/';
        }
    }
    renderDate(date) {
        if (!date) {
            return null;
        }
        const d = new Date(date);
        return (<strong>
        <dateTime_1.default date={d}/>
      </strong>);
    }
    renderEarly() {
        return (<React.Fragment>
        <Header>
          <h3>
            {(0, locale_1.t)('What are')}
            <i>{(0, locale_1.t)(' you ')}</i>
            {(0, locale_1.t)('doing here?')}
          </h3>
        </Header>
        <Body>
          <p>
            {(0, locale_1.t)("Not that its any of our business, but were you invited to this page? It's just that we don't exactly remember emailing you about it.")}
          </p>
          <p>{(0, locale_1.t)("Close this window and we'll email you when your download is ready.")}</p>
        </Body>
      </React.Fragment>);
    }
    renderExpired() {
        const { query } = this.state.download;
        const actionLink = this.getActionLink(query.type);
        return (<React.Fragment>
        <Header>
          <h3>{(0, locale_1.t)('This is awkward.')}</h3>
        </Header>
        <Body>
          <p>
            {(0, locale_1.t)("That link expired, so your download doesn't live here anymore. Just picked up one day and left town.")}
          </p>
          <p>
            {(0, locale_1.t)('Make a new one with your latest data. Your old download will never see it coming.')}
          </p>
          <DownloadButton href={actionLink} priority="primary">
            {(0, locale_1.t)('Start a New Download')}
          </DownloadButton>
        </Body>
      </React.Fragment>);
    }
    openInDiscover() {
        const { download: { query: { info }, }, } = this.state;
        const { orgId } = this.props.params;
        const to = {
            pathname: `/organizations/${orgId}/discover/results/`,
            query: info,
        };
        react_router_1.browserHistory.push(to);
    }
    renderOpenInDiscover() {
        const { download: { query = {
            type: dataExport_1.ExportQueryType.IssuesByTag,
            info: {},
        }, }, } = this.state;
        // default to IssuesByTag because we don't want to
        // display this unless we're sure its a discover query
        const { type = dataExport_1.ExportQueryType.IssuesByTag } = query;
        return type === 'Discover' ? (<React.Fragment>
        <p>{(0, locale_1.t)('Need to make changes?')}</p>
        <button_1.default priority="primary" onClick={() => this.openInDiscover()}>
          {(0, locale_1.t)('Open in Discover')}
        </button_1.default>
        <br />
      </React.Fragment>) : null;
    }
    renderValid() {
        const { download: { dateExpired, checksum }, } = this.state;
        const { orgId, dataExportId } = this.props.params;
        return (<React.Fragment>
        <Header>
          <h3>{(0, locale_1.t)('All done.')}</h3>
        </Header>
        <Body>
          <p>{(0, locale_1.t)("See, that wasn't so bad. Your data is all ready for download.")}</p>
          <button_1.default priority="primary" icon={<icons_1.IconDownload />} href={`/api/0/organizations/${orgId}/data-export/${dataExportId}/?download=true`}>
            {(0, locale_1.t)('Download CSV')}
          </button_1.default>
          <p>
            {(0, locale_1.t)("That link won't last forever — it expires:")}
            <br />
            {this.renderDate(dateExpired)}
          </p>
          {this.renderOpenInDiscover()}
          <p>
            <small>
              <strong>SHA1:{checksum}</strong>
            </small>
            <br />
            {(0, locale_1.tct)('Need help verifying? [link].', {
                link: (<a href="https://docs.sentry.io/product/discover-queries/query-builder/#filter-by-table-columns" target="_blank" rel="noopener noreferrer">
                  {(0, locale_1.t)('Check out our docs')}
                </a>),
            })}
          </p>
        </Body>
      </React.Fragment>);
    }
    renderError() {
        var _a;
        const { errors: { download: err }, } = this.state;
        const errDetail = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail;
        return (<layout_1.default>
        <main>
          <Header>
            <h3>
              {err.status} - {err.statusText}
            </h3>
          </Header>
          {errDetail && (<Body>
              <p>{errDetail}</p>
            </Body>)}
        </main>
      </layout_1.default>);
    }
    renderContent() {
        const { download } = this.state;
        switch (download.status) {
            case DownloadStatus.Early:
                return this.renderEarly();
            case DownloadStatus.Expired:
                return this.renderExpired();
            default:
                return this.renderValid();
        }
    }
    renderBody() {
        return (<layout_1.default>
        <main>{this.renderContent()}</main>
      </layout_1.default>);
    }
}
const Header = (0, styled_1.default)('header') `
  border-bottom: 1px solid ${p => p.theme.border};
  padding: ${(0, space_1.default)(3)} 40px 0;
  h3 {
    font-size: 24px;
    margin: 0 0 ${(0, space_1.default)(3)} 0;
  }
`;
const Body = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)} 40px;
  max-width: 500px;
  p {
    margin: ${(0, space_1.default)(1.5)} 0;
  }
`;
const DownloadButton = (0, styled_1.default)(button_1.default) `
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
exports.default = DataDownload;
//# sourceMappingURL=dataDownload.jsx.map