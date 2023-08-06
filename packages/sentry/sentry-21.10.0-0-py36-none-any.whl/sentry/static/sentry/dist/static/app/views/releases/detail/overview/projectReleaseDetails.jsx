Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const keyValueTable_1 = require("app/components/keyValueTable");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const locale_1 = require("app/locale");
const styles_1 = require("./styles");
const ProjectReleaseDetails = ({ release, releaseMeta, orgSlug, projectSlug }) => {
    var _a;
    const { version, versionInfo, dateCreated, firstEvent, lastEvent } = release;
    return (<styles_1.Wrapper>
      <styles_1.SectionHeading>{(0, locale_1.t)('Project Release Details')}</styles_1.SectionHeading>
      <keyValueTable_1.KeyValueTable>
        <keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Created')} value={<dateTime_1.default date={dateCreated} seconds={false}/>}/>
        <keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Version')} value={<version_1.default version={version} anchor={false}/>}/>
        <keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Package')} value={<StyledTextOverflow ellipsisDirection="left">
              {(_a = versionInfo.package) !== null && _a !== void 0 ? _a : '\u2014'}
            </StyledTextOverflow>}/>
        <keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('First Event')} value={firstEvent ? <timeSince_1.default date={firstEvent}/> : '\u2014'}/>
        <keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Last Event')} value={lastEvent ? <timeSince_1.default date={lastEvent}/> : '\u2014'}/>
        <keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Source Maps')} value={<link_1.default to={`/settings/${orgSlug}/projects/${projectSlug}/source-maps/${encodeURIComponent(version)}/`}>
              <count_1.default value={releaseMeta.releaseFileCount}/>{' '}
              {(0, locale_1.tn)('artifact', 'artifacts', releaseMeta.releaseFileCount)}
            </link_1.default>}/>
      </keyValueTable_1.KeyValueTable>
    </styles_1.Wrapper>);
};
const StyledTextOverflow = (0, styled_1.default)(textOverflow_1.default) `
  line-height: inherit;
  text-align: right;
`;
exports.default = ProjectReleaseDetails;
//# sourceMappingURL=projectReleaseDetails.jsx.map