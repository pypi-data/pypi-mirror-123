Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const queryString = (0, tslib_1.__importStar)(require("query-string"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const pill_1 = (0, tslib_1.__importDefault)(require("app/components/pill"));
const versionHoverCard_1 = (0, tslib_1.__importDefault)(require("app/components/versionHoverCard"));
const icons_1 = require("app/icons");
const utils_1 = require("app/utils");
const eventTagsPillValue_1 = (0, tslib_1.__importDefault)(require("./eventTagsPillValue"));
const iconStyle = (0, react_1.css) `
  position: relative;
  top: 1px;
`;
const EventTagsPill = ({ tag, query, organization, projectId, streamPath, releasesPath, }) => {
    const locationSearch = `?${queryString.stringify(query)}`;
    const { key, value } = tag;
    const isRelease = key === 'release';
    const name = !key ? <annotatedText_1.default value={key} meta={(0, metaProxy_1.getMeta)(tag, 'key')}/> : key;
    const type = !key ? 'error' : undefined;
    return (<pill_1.default name={name} value={value} type={type}>
      <eventTagsPillValue_1.default tag={tag} meta={(0, metaProxy_1.getMeta)(tag, 'value')} streamPath={streamPath} locationSearch={locationSearch} isRelease={isRelease}/>
      {(0, utils_1.isUrl)(value) && (<externalLink_1.default href={value} className="external-icon">
          <icons_1.IconOpen size="xs" css={iconStyle}/>
        </externalLink_1.default>)}
      {isRelease && (<div className="pill-icon">
          <versionHoverCard_1.default organization={organization} projectSlug={projectId} releaseVersion={value}>
            <link_1.default to={{ pathname: `${releasesPath}${value}/`, search: locationSearch }}>
              <icons_1.IconInfo size="xs" css={iconStyle}/>
            </link_1.default>
          </versionHoverCard_1.default>
        </div>)}
    </pill_1.default>);
};
exports.default = EventTagsPill;
//# sourceMappingURL=eventTagsPill.jsx.map