Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/events/styles");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const screenshot_1 = (0, tslib_1.__importDefault)(require("./screenshot"));
const tags_1 = (0, tslib_1.__importDefault)(require("./tags"));
function EventTagsAndScreenshots({ projectId: projectSlug, location, event, attachments, onDeleteScreenshot, organization, isShare = false, isBorderless = false, hasContext = false, }) {
    const { tags = [] } = event;
    const screenshot = attachments.find(({ name }) => name === 'screenshot.jpg' || name === 'screenshot.png');
    if (!tags.length && !hasContext && (isShare || !screenshot)) {
        return null;
    }
    return (<Wrapper isBorderless={isBorderless}>
      {!isShare && !!screenshot && (<screenshot_1.default organization={organization} event={event} projectSlug={projectSlug} screenshot={screenshot} onDelete={onDeleteScreenshot}/>)}
      {(!!tags.length || hasContext) && (<tags_1.default organization={organization} event={event} projectSlug={projectSlug} hasContext={hasContext} location={location}/>)}
    </Wrapper>);
}
exports.default = EventTagsAndScreenshots;
const Wrapper = (0, styled_1.default)(styles_1.DataSection) `
  display: grid;
  grid-gap: ${(0, space_1.default)(3)};

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    && {
      padding: 0;
      border: 0;
    }
  }

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    padding-bottom: ${(0, space_1.default)(2)};
    grid-template-columns: 1fr auto;
    grid-gap: ${(0, space_1.default)(4)};

    > *:first-child {
      border-bottom: 0;
      padding-bottom: 0;
    }
  }

  ${p => p.isBorderless &&
    `
    && {
        padding: ${(0, space_1.default)(3)} 0 0 0;
        :first-child {
          padding-top: 0;
          border-top: 0;
        }
      }
    `}
`;
//# sourceMappingURL=index.jsx.map