Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const utils_1 = require("app/components/events/interfaces/utils");
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const contextSummaryNoSummary_1 = (0, tslib_1.__importDefault)(require("./contextSummaryNoSummary"));
const item_1 = (0, tslib_1.__importDefault)(require("./item"));
const ContextSummaryUser = ({ data }) => {
    const user = (0, utils_1.removeFilterMaskedEntries)(data);
    if (Object.keys(user).length === 0) {
        return <contextSummaryNoSummary_1.default title={(0, locale_1.t)('Unknown User')}/>;
    }
    const renderUserDetails = (key) => {
        const userDetails = {
            subject: (0, locale_1.t)('Username:'),
            value: user.username,
            meta: (0, metaProxy_1.getMeta)(data, 'username'),
        };
        if (key === 'id') {
            userDetails.subject = (0, locale_1.t)('ID:');
            userDetails.value = user.id;
            userDetails.meta = (0, metaProxy_1.getMeta)(data, 'id');
        }
        return (<textOverflow_1.default isParagraph data-test-id="context-sub-title">
        <Subject>{userDetails.subject}</Subject>
        <annotatedText_1.default value={userDetails.value} meta={userDetails.meta}/>
      </textOverflow_1.default>);
    };
    const getUserTitle = () => {
        if (user.email) {
            return {
                value: user.email,
                meta: (0, metaProxy_1.getMeta)(data, 'email'),
            };
        }
        if (user.ip_address) {
            return {
                value: user.ip_address,
                meta: (0, metaProxy_1.getMeta)(data, 'ip_address'),
            };
        }
        if (user.id) {
            return {
                value: user.id,
                meta: (0, metaProxy_1.getMeta)(data, 'id'),
            };
        }
        if (user.username) {
            return {
                value: user.username,
                meta: (0, metaProxy_1.getMeta)(data, 'username'),
            };
        }
        return undefined;
    };
    const userTitle = getUserTitle();
    if (!userTitle) {
        return <contextSummaryNoSummary_1.default title={(0, locale_1.t)('Unknown User')}/>;
    }
    const icon = userTitle ? (<userAvatar_1.default user={user} size={32} className="context-item-icon" gravatar={false}/>) : (<span className="context-item-icon"/>);
    return (<item_1.default className="user" icon={icon}>
      {userTitle && (<h3 data-test-id="user-title">
          <annotatedText_1.default value={userTitle.value} meta={userTitle.meta}/>
        </h3>)}
      {user.id && user.id !== (userTitle === null || userTitle === void 0 ? void 0 : userTitle.value)
            ? renderUserDetails('id')
            : user.username &&
                user.username !== (userTitle === null || userTitle === void 0 ? void 0 : userTitle.value) &&
                renderUserDetails('username')}
    </item_1.default>);
};
exports.default = ContextSummaryUser;
const Subject = (0, styled_1.default)('strong') `
  margin-right: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=contextSummaryUser.jsx.map