Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const fileSize_1 = (0, tslib_1.__importDefault)(require("app/components/fileSize"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
/**
 * Render metadata about the event and provide a link to the JSON blob.
 * Used in the sidebar of performance event details and discover2 event details.
 */
function EventMetadata({ event, organization, projectId }) {
    const eventJsonUrl = `/api/0/projects/${organization.slug}/${projectId}/events/${event.eventID}/json/`;
    return (<MetaDataID>
      <styles_1.SectionHeading>{(0, locale_1.t)('Event ID')}</styles_1.SectionHeading>
      <MetadataContainer data-test-id="event-id">{event.eventID}</MetadataContainer>
      <MetadataContainer>
        <dateTime_1.default date={(0, getDynamicText_1.default)({
            value: event.dateCreated || (event.endTimestamp || 0) * 1000,
            fixed: 'Dummy timestamp',
        })}/>
      </MetadataContainer>
      <projects_1.default orgId={organization.slug} slugs={[projectId]}>
        {({ projects }) => {
            const project = projects.find(p => p.slug === projectId);
            return (<StyledProjectBadge project={project ? project : { slug: projectId }} avatarSize={16}/>);
        }}
      </projects_1.default>
      <MetadataJSON href={eventJsonUrl} className="json-link">
        {(0, locale_1.t)('Preview JSON')} (<fileSize_1.default bytes={event.size}/>)
      </MetadataJSON>
    </MetaDataID>);
}
const MetaDataID = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(4)};
`;
const MetadataContainer = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  font-size: ${p => p.theme.fontSizeMedium};
`;
const MetadataJSON = (0, styled_1.default)(externalLink_1.default) `
  font-size: ${p => p.theme.fontSizeMedium};
`;
const StyledProjectBadge = (0, styled_1.default)(projectBadge_1.default) `
  margin-bottom: ${(0, space_1.default)(2)};
`;
exports.default = EventMetadata;
//# sourceMappingURL=eventMetadata.jsx.map