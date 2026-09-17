import landing from './landing'
import brand from './brand'
import common from './common'
import dashboard from './dashboard'
import channelMonitorV2 from './channelMonitorV2'
import channelMonitorV3 from './channelMonitorV3'
import batchImage from './batchImage'
import cfAllowlist from './cfAllowlist'
import admin from './admin'
import misc from './misc'

export default {
  ...landing,
  ...brand,
  ...common,
  ...dashboard,
  ...channelMonitorV2,
  ...channelMonitorV3,
  ...batchImage,
  ...cfAllowlist,
  admin,
  ...misc,
}
