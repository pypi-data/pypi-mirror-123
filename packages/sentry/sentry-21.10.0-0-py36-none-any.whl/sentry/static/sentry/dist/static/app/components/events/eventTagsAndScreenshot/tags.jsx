Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const eventDataSection_1 = require("app/components/events/eventDataSection");
const locale_1 = require("app/locale");
const eventTags_1 = (0, tslib_1.__importDefault)(require("../eventTags/eventTags"));
const dataSection_1 = (0, tslib_1.__importDefault)(require("./dataSection"));
const tagsHighlight_1 = (0, tslib_1.__importDefault)(require("./tagsHighlight"));
function Tags({ event, organization, projectSlug, location, hasContext }) {
    return (<StyledDataSection title={(0, locale_1.t)('Tags')} description={(0, locale_1.t)('Tags help you quickly both access related events and view the tag distribution for a set of events')} data-test-id="event-tags">
      {hasContext && <tagsHighlight_1.default event={event}/>}
      <eventTags_1.default event={event} organization={organization} projectId={projectSlug} location={location}/>
    </StyledDataSection>);
}
exports.default = Tags;
const StyledDataSection = (0, styled_1.default)(dataSection_1.default) `
  overflow: hidden;
  ${eventDataSection_1.SectionContents} {
    overflow: hidden;
  }
`;
//# sourceMappingURL=tags.jsx.map