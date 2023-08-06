Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const formContext_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formContext"));
const constants_1 = require("app/views/settings/organizationDeveloperSettings/constants");
const subscriptionBox_1 = (0, tslib_1.__importDefault)(require("app/views/settings/organizationDeveloperSettings/subscriptionBox"));
class Subscriptions extends react_1.Component {
    constructor(props, context) {
        super(props, context);
        this.onChange = (resource, checked) => {
            const events = new Set(this.props.events);
            checked ? events.add(resource) : events.delete(resource);
            this.save(Array.from(events));
        };
        this.save = (events) => {
            this.props.onChange(events);
            this.context.form.setValue('events', events);
        };
        this.context.form.setValue('events', this.props.events);
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        // if webhooks are disabled, unset the events
        if (nextProps.webhookDisabled && this.props.events.length) {
            this.save([]);
        }
    }
    componentDidUpdate() {
        const { permissions, events } = this.props;
        const permittedEvents = events.filter(resource => permissions[constants_1.PERMISSIONS_MAP[resource]] !== 'no-access');
        if (JSON.stringify(events) !== JSON.stringify(permittedEvents)) {
            this.save(permittedEvents);
        }
    }
    render() {
        const { permissions, webhookDisabled, events } = this.props;
        return (<SubscriptionGrid>
        {constants_1.EVENT_CHOICES.map(choice => {
                const disabledFromPermissions = permissions[constants_1.PERMISSIONS_MAP[choice]] === 'no-access';
                return (<react_1.Fragment key={choice}>
              <subscriptionBox_1.default key={choice} disabledFromPermissions={disabledFromPermissions} webhookDisabled={webhookDisabled} checked={events.includes(choice) && !disabledFromPermissions} resource={choice} onChange={this.onChange}/>
            </react_1.Fragment>);
            })}
      </SubscriptionGrid>);
    }
}
exports.default = Subscriptions;
Subscriptions.defaultProps = {
    webhookDisabled: false,
};
Subscriptions.contextType = formContext_1.default;
const SubscriptionGrid = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
`;
//# sourceMappingURL=resourceSubscriptions.jsx.map