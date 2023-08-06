Object.defineProperty(exports, "__esModule", { value: true });
exports.addRepository = exports.migrateRepository = exports.cancelDeleteRepository = exports.deleteRepository = exports.addIntegrationToProject = exports.removeIntegrationFromProject = void 0;
const indicator_1 = require("app/actionCreators/indicator");
const api_1 = require("app/api");
const locale_1 = require("app/locale");
const api = new api_1.Client();
/**
 * Removes an integration from a project.
 *
 * @param {String} orgId Organization Slug
 * @param {String} projectId Project Slug
 * @param {Object} integration The organization integration to remove
 */
function removeIntegrationFromProject(orgId, projectId, integration) {
    const endpoint = `/projects/${orgId}/${projectId}/integrations/${integration.id}/`;
    (0, indicator_1.addLoadingMessage)();
    return api.requestPromise(endpoint, { method: 'DELETE' }).then(() => {
        (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Disabled %s for %s', integration.name, projectId));
    }, () => {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to disable %s for %s', integration.name, projectId));
    });
}
exports.removeIntegrationFromProject = removeIntegrationFromProject;
/**
 * Add an integration to a project
 *
 * @param {String} orgId Organization Slug
 * @param {String} projectId Project Slug
 * @param {Object} integration The organization integration to add
 */
function addIntegrationToProject(orgId, projectId, integration) {
    const endpoint = `/projects/${orgId}/${projectId}/integrations/${integration.id}/`;
    (0, indicator_1.addLoadingMessage)();
    return api.requestPromise(endpoint, { method: 'PUT' }).then(() => {
        (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Enabled %s for %s', integration.name, projectId));
    }, () => {
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to enabled %s for %s', integration.name, projectId));
    });
}
exports.addIntegrationToProject = addIntegrationToProject;
/**
 * Delete a respository
 *
 * @param {Object} client ApiClient
 * @param {String} orgId Organization Slug
 * @param {String} repositoryId Repository ID
 */
function deleteRepository(client, orgId, repositoryId) {
    (0, indicator_1.addLoadingMessage)();
    const promise = client.requestPromise(`/organizations/${orgId}/repos/${repositoryId}/`, {
        method: 'DELETE',
    });
    promise.then(() => (0, indicator_1.clearIndicators)(), () => (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to delete repository.')));
    return promise;
}
exports.deleteRepository = deleteRepository;
/**
 * Cancel the deletion of a respository
 *
 * @param {Object} client ApiClient
 * @param {String} orgId Organization Slug
 * @param {String} repositoryId Repository ID
 */
function cancelDeleteRepository(client, orgId, repositoryId) {
    (0, indicator_1.addLoadingMessage)();
    const promise = client.requestPromise(`/organizations/${orgId}/repos/${repositoryId}/`, {
        method: 'PUT',
        data: { status: 'visible' },
    });
    promise.then(() => (0, indicator_1.clearIndicators)(), () => (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to cancel deletion.')));
    return promise;
}
exports.cancelDeleteRepository = cancelDeleteRepository;
function applyRepositoryAddComplete(promise) {
    promise.then((repo) => {
        const message = (0, locale_1.tct)('[repo] has been successfully added.', {
            repo: repo.name,
        });
        (0, indicator_1.addSuccessMessage)(message);
    }, errorData => {
        const text = errorData.responseJSON.errors
            ? errorData.responseJSON.errors.__all__
            : (0, locale_1.t)('Unable to add repository.');
        (0, indicator_1.addErrorMessage)(text);
    });
    return promise;
}
/**
 * Migrate a repository to a new integration.
 *
 * @param {Object} client ApiClient
 * @param {String} orgId Organization Slug
 * @param {String} repositoryId Repository ID
 * @param {Object} integration Integration provider data.
 */
function migrateRepository(client, orgId, repositoryId, integration) {
    const data = { integrationId: integration.id };
    (0, indicator_1.addLoadingMessage)();
    const promise = client.requestPromise(`/organizations/${orgId}/repos/${repositoryId}/`, {
        data,
        method: 'PUT',
    });
    return applyRepositoryAddComplete(promise);
}
exports.migrateRepository = migrateRepository;
/**
 * Add a repository
 *
 * @param {Object} client ApiClient
 * @param {String} orgId Organization Slug
 * @param {String} name Repository identifier/name to add
 * @param {Object} integration Integration provider data.
 */
function addRepository(client, orgId, name, integration) {
    const data = {
        installation: integration.id,
        identifier: name,
        provider: `integrations:${integration.provider.key}`,
    };
    (0, indicator_1.addLoadingMessage)();
    const promise = client.requestPromise(`/organizations/${orgId}/repos/`, {
        method: 'POST',
        data,
    });
    return applyRepositoryAddComplete(promise);
}
exports.addRepository = addRepository;
//# sourceMappingURL=integrations.jsx.map