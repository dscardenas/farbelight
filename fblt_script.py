import bpy

def createVoronoiGroup():

    # create voronoi node group
    farbelight = bpy.data.node_groups.new(name="farbelight", type="ShaderNodeTree")


    # add all required nodes and adjust settings
    add1 = farbelight.nodes.new('ShaderNodeMix')
    add1.data_type = 'RGBA'
    add1.blend_type = 'ADD'

    ramp1 = farbelight.nodes.new('ShaderNodeValToRGB')
    ramp1.color_ramp.interpolation =  'CONSTANT'
    ramp1.color_ramp.elements[1].position = .332

    voronoi1 = farbelight.nodes.new('ShaderNodeTexVoronoi')
    voronoi1.voronoi_dimensions = '2D'
    voronoi1.inputs[2].default_value = 200
    voronoi1.inputs[8].default_value = 0

    map1 = farbelight.nodes.new('ShaderNodeMapping')

    coord1 = farbelight.nodes.new('ShaderNodeTexCoord')

    ramp2 = farbelight.nodes.new('ShaderNodeValToRGB')
    ramp2.color_ramp.interpolation =  'CONSTANT'
    ramp2.color_ramp.elements[1].position = .332

    voronoi2 = farbelight.nodes.new('ShaderNodeTexVoronoi')
    voronoi2.voronoi_dimensions = '2D'
    voronoi2.inputs[2].default_value = 200
    voronoi2.inputs[8].default_value = 0

    map2 = farbelight.nodes.new('ShaderNodeMapping')

    coord2 = farbelight.nodes.new('ShaderNodeTexCoord')

    # create group output
    groupoutput = farbelight.nodes.new('NodeGroupOutput')
    result_output = farbelight.interface.new_socket(
        name="Result",
        description="output",
        in_out='OUTPUT',
        socket_type='NodeSocketColor'
        )

    # link all nodes
    farbelight.links.new(coord1.outputs[5], map1.inputs[0])
    farbelight.links.new(map1.outputs[0], voronoi1.inputs[0])
    farbelight.links.new(voronoi1.outputs[0], ramp1.inputs[0])
    farbelight.links.new(ramp1.outputs['Color'], add1.inputs['A'])

    farbelight.links.new(coord2.outputs[5], map2.inputs[0])
    farbelight.links.new(map2.outputs[0], voronoi2.inputs[0])
    farbelight.links.new(voronoi2.outputs[1], ramp2.inputs[0])
    farbelight.links.new(ramp2.outputs['Color'], add1.inputs['B'])

    farbelight.links.new(add1.outputs['Result'], groupoutput.inputs['Result'])

    return farbelight


for material in bpy.data.materials:
    material.use_nodes = True
    if material.name.contains('flbt_') == False or material.node_tree.nodes.contains('') == False:
        name = material.name
        material.name = 'flbt_' + name
        bsdf = material.node_tree.nodes.get('ShaderNodeBsdfPrincipled')
        mat_out = material.node_tree.nodes.get('ShaderNodeOutputMaterial')
        farbelight_node = material.node_tree.nodes.new('ShaderNodeGroup')
        farbelight_node.location = (325, 137)
        farbelight_node.node_tree = createVoronoiGroup()
        linlight = material.node_tree.nodes.new('ShaderNodeMix')
        linlight.data_type = 'RGBA'
        linlight.blend_type = 'LINEAR_LIGHT'
        linlight.inputs[0].default_value = .208
        linlight.location = (400, 150)
        shadertoRGB = material.node_tree.nodes.new('ShaderNodeShaderToRGB')
        shadertoRGB.location = (525,319)
        ramp = material.node_tree.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.interpolation =  'CONSTANT'
        ramp.color_ramp.elements.new(.5)
        ramp.location = (661,200)
        
        material.links.new(farbelight_node.outputs[0], linlight.inputs['A'])
        material.links.new(linlight.outputs[0], bsdf.inputs[0])
        material.links.new(bsdf.outputs[0], shadertoRGB.inputs[0])
        material.links.new(shadertoRGB.outputs[0], ramp.inputs[0])
        material.links.new(ramp.outputs[0], mat_out.inputs[0])
