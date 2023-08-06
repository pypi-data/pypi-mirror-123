import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { requestAPI } from './handler';

/**
 * Initialization data for the structured_text extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'structured_text:plugin',
  autoStart: true,
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, settingRegistry: ISettingRegistry | null) => {
    console.log('JupyterLab extension structured_text is activated!');

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('structured_text settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for structured_text.', reason);
        });
    }

    requestAPI<any>('get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The structured_text server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
