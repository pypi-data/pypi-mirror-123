Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const numberField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/numberField"));
const radioField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/radioField"));
const impacts = [
    (0, locale_1.tct)("[strong:Quota applies.] Every event you choose to reprocess counts against your plan's quota. Rate limits and spike protection do not apply.", { strong: <strong /> }),
    (0, locale_1.tct)('[strong:Attachment storage required.] If your events come from minidumps or unreal crash reports, you must have [link:attachment storage] enabled.', {
        strong: <strong />,
        link: (<externalLink_1.default href="https://docs.sentry.io/platforms/native/enriching-events/attachments/#crash-reports-and-privacy"/>),
    }),
    (0, locale_1.t)('Please wait one hour after upload before attempting to reprocess missing debug files.'),
];
const remainingEventsChoices = [
    ['keep', (0, locale_1.t)('Keep')],
    ['delete', (0, locale_1.t)('Delete')],
];
class ReprocessingEventModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = { maxEvents: undefined };
        this.handleSuccess = () => {
            const { closeModal } = this.props;
            closeModal();
            window.location.reload();
        };
        this.handleMaxEventsChange = (maxEvents) => {
            this.setState({ maxEvents: Number(maxEvents) || undefined });
        };
    }
    handleError() {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to reprocess. Please check your input.'));
    }
    render() {
        const { organization, Header, Body, closeModal, groupId } = this.props;
        const { maxEvents } = this.state;
        const orgSlug = organization.slug;
        const endpoint = `/organizations/${orgSlug}/issues/${groupId}/reprocessing/`;
        const title = (0, locale_1.t)('Reprocess Events');
        return (<react_1.Fragment>
        <Header closeButton>{title}</Header>
        <Body>
          <Introduction>
            {(0, locale_1.t)('Reprocessing applies new debug files and grouping enhancements to this Issue. Please consider these impacts:')}
          </Introduction>
          <StyledList symbol="bullet">
            {impacts.map((impact, index) => (<listItem_1.default key={index}>{impact}</listItem_1.default>))}
          </StyledList>
          <Introduction>
            {(0, locale_1.tct)('For more information, please refer to [link:the documentation.]', {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/error-monitoring/reprocessing/"/>),
            })}
          </Introduction>
          <form_1.default submitLabel={title} apiEndpoint={endpoint} apiMethod="POST" initialData={{ maxEvents: undefined, remainingEvents: 'keep' }} onSubmitSuccess={this.handleSuccess} onSubmitError={this.handleError} onCancel={closeModal} footerClass="modal-footer">
            <numberField_1.default name="maxEvents" label={(0, locale_1.t)('Number of events to be reprocessed')} help={(0, locale_1.t)('If you set a limit, we will reprocess your most recent events.')} placeholder={(0, locale_1.t)('Reprocess all events')} onChange={this.handleMaxEventsChange} min={1}/>

            <radioField_1.default orientInline label={(0, locale_1.t)('Remaining events')} help={(0, locale_1.t)('What to do with the events that are not reprocessed.')} name="remainingEvents" choices={remainingEventsChoices} disabled={maxEvents === undefined}/>
          </form_1.default>
        </Body>
      </react_1.Fragment>);
    }
}
exports.default = ReprocessingEventModal;
const Introduction = (0, styled_1.default)('p') `
  font-size: ${p => p.theme.fontSizeLarge};
`;
const StyledList = (0, styled_1.default)(list_1.default) `
  grid-gap: ${(0, space_1.default)(1)};
  margin-bottom: ${(0, space_1.default)(4)};
  font-size: ${p => p.theme.fontSizeMedium};
`;
//# sourceMappingURL=reprocessEventModal.jsx.map