Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const groupBy_1 = (0, tslib_1.__importDefault)(require("lodash/groupBy"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const indicator_1 = require("app/actionCreators/indicator");
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const panels_1 = require("app/components/panels");
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const ENDPOINT = '/users/me/subscriptions/';
class AccountSubscriptions extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleToggle = (subscription, index, _e) => {
            const subscribed = !subscription.subscribed;
            const oldSubscriptions = this.state.subscriptions;
            this.setState(state => {
                const newSubscriptions = state.subscriptions.slice();
                newSubscriptions[index] = Object.assign(Object.assign({}, subscription), { subscribed, subscribedDate: new Date().toString() });
                return Object.assign(Object.assign({}, state), { subscriptions: newSubscriptions });
            });
            this.api.request(ENDPOINT, {
                method: 'PUT',
                data: {
                    listId: subscription.listId,
                    subscribed,
                },
                success: () => {
                    (0, indicator_1.addSuccessMessage)(`${subscribed ? 'Subscribed' : 'Unsubscribed'} to ${subscription.listName}`);
                },
                error: () => {
                    (0, indicator_1.addErrorMessage)(`Unable to ${subscribed ? '' : 'un'}subscribe to ${subscription.listName}`);
                    this.setState({ subscriptions: oldSubscriptions });
                },
            });
        };
    }
    getEndpoints() {
        return [['subscriptions', ENDPOINT]];
    }
    getTitle() {
        return 'Subscriptions';
    }
    renderBody() {
        const subGroups = Object.entries((0, groupBy_1.default)(this.state.subscriptions, sub => sub.email));
        return (<div>
        <settingsPageHeader_1.default title="Subscriptions"/>
        <textBlock_1.default>
          {(0, locale_1.t)(`Sentry is committed to respecting your inbox. Our goal is to
              provide useful content and resources that make fixing errors less
              painful. Enjoyable even.`)}
        </textBlock_1.default>

        <textBlock_1.default>
          {(0, locale_1.t)(`As part of our compliance with the EU’s General Data Protection
              Regulation (GDPR), starting on 25 May 2018, we’ll only email you
              according to the marketing categories to which you’ve explicitly
              opted-in.`)}
        </textBlock_1.default>

        <panels_1.Panel>
          {this.state.subscriptions.length ? (<div>
              <panels_1.PanelHeader>{(0, locale_1.t)('Subscription')}</panels_1.PanelHeader>
              <panels_1.PanelBody>
                {subGroups.map(([email, subscriptions]) => (<React.Fragment key={email}>
                    {subGroups.length > 1 && (<Heading>
                        <icons_1.IconToggle /> {(0, locale_1.t)('Subscriptions for %s', email)}
                      </Heading>)}

                    {subscriptions.map((subscription, index) => (<panels_1.PanelItem center key={subscription.listId}>
                        <SubscriptionDetails>
                          <SubscriptionName>{subscription.listName}</SubscriptionName>
                          {subscription.listDescription && (<Description>{subscription.listDescription}</Description>)}
                          {subscription.subscribed ? (<SubscribedDescription>
                              <div>
                                {(0, locale_1.tct)('[email] on [date]', {
                                email: subscription.email,
                                date: (<dateTime_1.default shortDate date={(0, moment_1.default)(subscription.subscribedDate)}/>),
                            })}
                              </div>
                            </SubscribedDescription>) : (<SubscribedDescription>
                              {(0, locale_1.t)('Not currently subscribed')}
                            </SubscribedDescription>)}
                        </SubscriptionDetails>
                        <div>
                          <switchButton_1.default isActive={subscription.subscribed} size="lg" toggle={this.handleToggle.bind(this, subscription, index)}/>
                        </div>
                      </panels_1.PanelItem>))}
                  </React.Fragment>))}
              </panels_1.PanelBody>
            </div>) : (<emptyMessage_1.default>{(0, locale_1.t)("There's no subscription backend present.")}</emptyMessage_1.default>)}
        </panels_1.Panel>
        <textBlock_1.default>
          {(0, locale_1.t)(`We’re applying GDPR consent and privacy policies to all Sentry
              contacts, regardless of location. You’ll be able to manage your
              subscriptions here and from an Unsubscribe link in the footer of
              all marketing emails.`)}
        </textBlock_1.default>

        <textBlock_1.default>
          {(0, locale_1.tct)('Please contact [email:learn@sentry.io] with any questions or suggestions.', { email: <a href="mailto:learn@sentry.io"/> })}
        </textBlock_1.default>
      </div>);
    }
}
const Heading = (0, styled_1.default)(panels_1.PanelItem) `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  font-size: ${p => p.theme.fontSizeMedium};
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};
  background: ${p => p.theme.backgroundSecondary};
  color: ${p => p.theme.subText};
`;
const SubscriptionDetails = (0, styled_1.default)('div') `
  width: 50%;
  padding-right: ${(0, space_1.default)(2)};
`;
const SubscriptionName = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;
const Description = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  margin-top: ${(0, space_1.default)(0.75)};
  color: ${p => p.theme.subText};
`;
const SubscribedDescription = (0, styled_1.default)(Description) `
  color: ${p => p.theme.gray300};
`;
exports.default = AccountSubscriptions;
//# sourceMappingURL=accountSubscriptions.jsx.map