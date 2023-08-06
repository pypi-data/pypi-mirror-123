#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from gym.envs.registration import register

register(
    id='update1-v0',
    entry_point='gym_update1.envs:UpdateEnv1',
)

